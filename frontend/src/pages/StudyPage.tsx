import { type StudyCoverage, type StudyResponse, fetchJson } from "../api";
import { useApi } from "../useApi";

type StudyPageProps = {
  unitId: string;
};

const coverageStatusLabel: Record<StudyCoverage["status"], string> = {
  missing: "Missing",
  partial: "Partial",
  covered: "Covered",
};

export function StudyPage({ unitId }: StudyPageProps) {
  const state = useApi(unitId, (signal) =>
    fetchJson<StudyResponse>(`/api/study/units/${unitId}`, signal),
  );
  const study = state.status === "ready" ? state.data : null;

  return (
    <main>
      {state.status === "loading" && <p>Loading study material…</p>}

      {state.status === "error" && <p>Unable to load study material.</p>}

      {study && (
        <>
          <h1>{study.programme_unit.title}</h1>
          <p>Knowledge need: {study.knowledge_need.title}</p>

          <section aria-labelledby="study-coverage-heading">
            <h2 id="study-coverage-heading">Study coverage</h2>
            <p>
              {coverageStatusLabel[study.coverage.status]} · {study.coverage.covered_count} of {study.coverage.required_count} aspects covered ({study.coverage.coverage_percentage}%)
            </p>

            <h3>Study aspects</h3>
            <ul>
              {study.coverage.required_aspects.map((aspect) => {
                const covered = study.coverage.covered_aspects.includes(aspect);

                return (
                  <li key={aspect}>
                    <span>{covered ? "Covered" : "Pending"}</span> · {aspect}
                  </li>
                );
              })}
            </ul>
          </section>

          <section aria-labelledby="study-material-heading">
            <h2 id="study-material-heading">Study material</h2>
            <div style={{ whiteSpace: "pre-wrap" }}>{study.study_material}</div>
          </section>

          <section aria-labelledby="study-sources-heading">
            <h2 id="study-sources-heading">Sources</h2>
            <ul>
              {study.sources.map((source) => (
                <li key={source.title}>
                  {source.locator ? (
                    <a href={source.locator} target="_blank" rel="noreferrer">
                      {source.title}
                    </a>
                  ) : (
                    <span>{source.title}</span>
                  )}
                </li>
              ))}
            </ul>
          </section>
        </>
      )}
    </main>
  );
}
