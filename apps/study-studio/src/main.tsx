import React from "react";
import ReactDOM from "react-dom/client";
import { Suspense, lazy } from "react";
import { LocaleProvider } from "./Locale";
const App = lazy(() => import("./App"));
import Pilot from "./Pilot";
import "katex/dist/katex.min.css";
import "./style.css";
ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    {new URLSearchParams(location.search).has("prototype") ? (
      <Suspense fallback={<p>Loading…</p>}>
        <App />
      </Suspense>
    ) : (
      <LocaleProvider>
        <Pilot />
      </LocaleProvider>
    )}
  </React.StrictMode>,
);
