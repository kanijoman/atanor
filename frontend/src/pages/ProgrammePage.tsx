import { type Programme, fetchJson } from "../api";
import { useApi } from "../useApi";

type ProgrammePageProps = {
  programmeId: string;
};

export function ProgrammePage({ programmeId }: ProgrammePageProps) {
  const state = useApi(programmeId, (signal) =>
    fetchJson<Programme>(`/api/study/programmes/${programmeId}`, signal),
  );

  return (
    <main>
      {state.status === "loading" && <p>Loading programme…</p>}

      {state.status === "error" && <p>Unable to load programme.</p>}

      {state.status === "ready" && (
        <>
          <h1>Programme {state.data.identifier}</h1>
          <p>{state.data.title}</p>

          {state.data.units.length === 0 ? (
            <p>No programme units are available yet.</p>
          ) : (
            <ul>
              {state.data.units.map((unit) => (
                <li key={unit.id}>
                  {unit.study_material_available ? (
                    <a href={`/study/${unit.id}`}>
                      {unit.number}. {unit.title}
                    </a>
                  ) : (
                    <span>
                      {unit.number}. {unit.title}
                    </span>
                  )}
                  <span>
                    {unit.study_material_available
                      ? "Study material available"
                      : "Study material not available"}
                  </span>
                </li>
              ))}
            </ul>
          )}
        </>
      )}
    </main>
  );
}
