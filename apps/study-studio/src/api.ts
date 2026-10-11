export async function api<T>(path:string, options:RequestInit={}):Promise<T>{
  let response:Response;
  try { response=await fetch('/api'+path,{...options,headers:options.body instanceof FormData?options.headers:{'Content-Type':'application/json',...options.headers}}); }
  catch { throw new Error('The local server is unavailable. Restart Learning Studio and try again; saved work stays on this computer.'); }
  if(!response.ok){let message='The request could not be completed.';try{const data=await response.json();message=typeof data.detail==='string'?data.detail:JSON.stringify(data.detail);}catch{/* Use safe fallback. */}throw new Error(message);}
  return response.json();
}
export const post=<T,>(path:string,body:unknown={})=>api<T>(path,{method:'POST',body:JSON.stringify(body)});
