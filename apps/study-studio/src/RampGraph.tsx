import { useId, useState } from "react";
import { guidedText, type TeachingLanguage } from "./guidedLocale";

export default function RampGraph({
  step,
  language,
}: {
  step: number;
  language: TeachingLanguage;
}) {
  const [time, setTime] = useState(step === 0 ? 0 : 5);
  const id = useId();
  const tx = guidedText[language];
  const x = (t: number) => 45 + t * 67;
  const y = (v: number) => 211 - v * (step === 0 ? 23 : 11.5);
  const r = (v: number) => Math.max(v, 0);
  const first = (t: number) => (step === 0 ? 1 : 2) * r(t - 1);
  const second = (t: number) => (step === 0 ? 0 : 2 * r(t - 4));
  const value = (t: number) =>
    first(t) - second(t) - (step === 2 && t >= 6 ? 6 : 0);
  const line = (points: number[][]) =>
    points.map(([t, v], i) => `${i ? "L" : "M"}${x(t)},${y(v)}`).join(" ");
  const f = (n: number) =>
    new Intl.NumberFormat(language, { maximumFractionDigits: 2 }).format(n);
  return (
    <figure className="guided-graph">
      <figcaption>{tx.graph}</figcaption>
      <p className="guided-formula">
        {step === 0
          ? "r(t−1)"
          : step === 1
            ? "y(t) = 2r(t−1) − 2r(t−4)"
            : "x(t) = 2r(t−1) − 2r(t−4) − 6u(t−6)"}
      </p>
      <svg viewBox="0 0 620 250" role="img" aria-labelledby={`${id}-title`}>
        <title id={`${id}-title`}>{tx.graphAlt}</title>
        <path d="M35,211 H598 M45,218 V15" stroke="#8b9b90" fill="none" />
        {[0, 1, 2, 4, 6, 8].map((t) => (
          <g key={t}>
            <path d={`M${x(t)},211 v5`} stroke="#839788" />
            <text x={x(t)} y={235} textAnchor="middle">
              {t}
            </text>
          </g>
        ))}
        {[2, 4, 6].map((v) => (
          <g key={v}>
            <path
              d={`M45,${y(v)} H582`}
              stroke="#d8e2d4"
              strokeDasharray="3 5"
            />
            <text x="30" y={y(v) + 4} textAnchor="end">
              {v}
            </text>
          </g>
        ))}
        <text x="598" y="228">
          t
        </text>
        {step > 0 && (
          <>
            <path
              d={line([
                [0, 0],
                [1, 0],
                [8, first(8)],
              ])}
              stroke="#818fbc"
              strokeWidth="2"
              strokeDasharray="7 5"
              fill="none"
            />
            <path
              d={line([
                [0, 0],
                [4, 0],
                [8, second(8)],
              ])}
              stroke="#a97638"
              strokeWidth="2"
              strokeDasharray="2 5"
              fill="none"
            />
          </>
        )}
        <path
          d={
            step === 0
              ? line([
                  [0, 0],
                  [1, 0],
                  [8, 7],
                ])
              : step === 1
                ? line([
                    [0, 0],
                    [1, 0],
                    [4, 6],
                    [8, 6],
                  ])
                : line([
                    [0, 0],
                    [1, 0],
                    [4, 6],
                    [6, 6],
                  ]) +
                  " " +
                  line([
                    [6, 0],
                    [8, 0],
                  ])
          }
          stroke="#215a44"
          strokeWidth="3.5"
          fill="none"
        />
        {step === 2 && (
          <>
            <path
              d={`M${x(6)},${y(6)} V${y(0)}`}
              stroke="#215a44"
              strokeDasharray="3 4"
            />
            <circle
              cx={x(6)}
              cy={y(6)}
              r="5"
              fill="#f6f8f0"
              stroke="#215a44"
              strokeWidth="2"
            />
            <circle cx={x(6)} cy={y(0)} r="5" fill="#215a44" />
          </>
        )}
        <path
          d={`M${x(time)},15 V211`}
          stroke="#5b786a"
          strokeDasharray="4 4"
        />
        <circle
          cx={x(time)}
          cy={y(value(time))}
          r="5"
          fill="#245c44"
          stroke="white"
          strokeWidth="2"
        />
      </svg>
      {step > 0 && (
        <div className="guided-legend">
          <span>┄ {tx.first}</span>
          <span>┈ {tx.second}</span>
          <span>━ {tx.result}</span>
        </div>
      )}
      <label htmlFor={`${id}-time`}>
        {tx.time}: {f(time)}
      </label>
      <input
        id={`${id}-time`}
        type="range"
        min="0"
        max="8"
        step="0.1"
        value={time}
        onChange={(e) => setTime(Number(e.target.value))}
      />
      <output className="guided-readout" aria-live="polite">
        {step === 0
          ? `t−1 = ${f(time - 1)}; r(t−1) = ${f(value(time))}`
          : `${tx.height}: ${f(value(time))}; ${tx.first}: ${f(first(time))}; ${tx.second}: ${f(second(time))}`}
      </output>
      <p>{tx.graphNote}</p>
      {step === 2 && <p>{tx.jump}</p>}
    </figure>
  );
}
