import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import Pilot from "./Pilot";
import "katex/dist/katex.min.css";
import "./style.css";
ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    {new URLSearchParams(location.search).has("prototype") ? (
      <App />
    ) : (
      <Pilot />
    )}
  </React.StrictMode>,
);
