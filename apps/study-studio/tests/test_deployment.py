"""Hosted boundary; all requests use synthetic credentials and an isolated database."""
import os
import unittest
from unittest.mock import patch
from datetime import datetime, timedelta, timezone
from fastapi.testclient import TestClient
import test_pilot as fixtures
from backend import app
from backend.deployment import settings
from backend.pilot import store

class DeploymentTests(unittest.TestCase):
    setUp=fixtures.PilotTests.setUp
    tearDown=fixtures.PilotTests.tearDown
    make=fixtures.PilotTests.make
    picture=fixtures.PilotTests.picture

    def hosted_env(self):
        return {'STUDIO_DEPLOYMENT':'hosted','STUDIO_PUBLIC_ORIGIN':'https://study.example.test','STUDIO_BOOTSTRAP_TOKEN':'synthetic-bootstrap-token-32-characters','STUDIO_DATA_DIR':'/tmp/synthetic-studio'}

    def test_fail_closed_and_exact_origin(self):
        self.assertFalse(settings({}).hosted)
        for update in ({'STUDIO_PUBLIC_ORIGIN':'http://study.test'}, {'STUDIO_BOOTSTRAP_TOKEN':''},{'STUDIO_DATA_DIR':'relative'},{'STUDIO_PUBLIC_ORIGIN':'https://user:pass@study.test'},{'STUDIO_PUBLIC_ORIGIN':'https://study.test/path'},{'STUDIO_PUBLIC_ORIGIN':'https://study.test?key=secret'}):
            with self.assertRaises(ValueError):settings({**self.hosted_env(),**update})
        cfg=settings(self.hosted_env());self.assertEqual(cfg.origins,('https://study.example.test',));self.assertNotIn('*',cfg.hosts)

    def test_bootstrap_requires_token_and_secure_cookie(self):
        from sqlalchemy import delete
        with store.engine.begin() as conn:conn.execute(delete(store.records).where(store.records.c.kind.in_(['user','login'])))
        body={'name':'HostedOwner','password':'synthetic-password'}
        with patch.dict(os.environ,self.hosted_env()),TestClient(app.app,base_url='https://localhost') as c:
            self.assertEqual(c.post('/api/pilot/auth/register',json=body).status_code,403)
            body['bootstrap_token']=self.hosted_env()['STUDIO_BOOTSTRAP_TOKEN']
            r=c.post('/api/pilot/auth/register',json=body);self.assertEqual(r.status_code,200);self.assertIn('Secure',r.headers['set-cookie'])
            status=c.get('/api/pilot/status').json();self.assertEqual(status['deployment'],'hosted-invitation');self.assertNotIn('bootstrap',str(status))
            self.assertEqual(c.post('/api/pilot/auth/register',json={**body,'name':'NoInvite'}).status_code,403)

    def test_hosted_origin_body_limits_and_legacy_boundary(self):
        with patch.object(app,'DEPLOYMENT',settings(self.hosted_env())):
            self.assertEqual(self.client.post('/api/pilot/auth/login',json={'name':'Owner','password':'safe-test-password'},headers={'origin':'http://127.0.0.1:8765'}).status_code,403)
            r=self.client.post('/api/pilot/auth/login',json={'name':'Owner','password':'safe-test-password'},headers={'origin':'https://study.example.test'})
            self.assertEqual(r.status_code,200);self.assertIn('Strict-Transport-Security',r.headers)
            self.assertEqual(self.client.get('/api/config').status_code,404)
            self.assertEqual(self.client.get('/api/health').status_code,200)
            self.assertEqual(self.client.post('/api/pilot/auth/login',content=b'x'*270000).status_code,413)

    def test_expired_invitation_and_pilot_capacity(self):
        token=self.client.post('/api/pilot/auth/invite').json()['invite']
        record=store.listing('invite','auth')[0];record['expires_at']=(datetime.now(timezone.utc)-timedelta(days=1)).isoformat();store.save('invite','auth',record)
        self.assertEqual(self.client.post('/api/pilot/auth/register',json={'name':'Expired','password':'synthetic-password','invite':token}).status_code,403)
        token=self.client.post('/api/pilot/auth/invite').json()['invite']
        with patch.dict(os.environ,{**self.hosted_env(),'STUDIO_MAX_USERS':'1'}):
            self.assertEqual(self.client.post('/api/pilot/auth/register',json={'name':'OverLimit','password':'synthetic-password','invite':token}).status_code,403)

    def test_invalid_password_not_echoed_and_english_error(self):
        r=self.client.post('/api/pilot/auth/login',json={'name':'Owner','password':'secret'},headers={'accept-language':'en'})
        self.assertEqual(r.status_code,422);self.assertNotIn('secret',r.text);self.assertIn('required',r.text)
        r=self.client.post('/api/pilot/auth/login',json={'name':'Owner','password':'wrong-password'},headers={'accept-language':'en'})
        self.assertEqual(r.json()['detail'],'Incorrect username or password.')

    def test_photo_quota_preserves_prior_upload(self):
        t=self.make();photo=self.picture(t)
        with patch.dict(os.environ,{'STUDIO_PHOTO_QUOTA_BYTES':'1'}):
            import io
            from PIL import Image
            b=io.BytesIO();Image.new('RGB',(10,10)).save(b,'PNG')
            r=self.client.post('/api/pilot/photos/'+t['id'],files={'file':('test.png',b.getvalue(),'image/png')});self.assertEqual(r.status_code,413)
        self.assertEqual(self.client.get('/api/pilot/photos/'+photo['id']).status_code,200)
