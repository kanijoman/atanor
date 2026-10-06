import { type Call, type CallProgramme, fetchJson } from "../api";
import { useApi } from "../useApi";

type CallPageProps = {
  callId: string;
};

export function CallPage({ callId }: CallPageProps) {
  const state = useApi(callId, async (signal) => {
    const [call, programmes] = await Promise.all([
      fetchJson<Call>(`/api/calls/${callId}`, signal),
      fetchJson<CallProgramme[]>(`/api/calls/${callId}/programmes`, signal),
    ]);

    return { call, programmes };
  });

  return (
    <main>
      {state.status === "loading" && <p>Loading call…</p>}

      {state.status === "error" && <p>Unable to load call.</p>}

      {state.status === "ready" && (
        <>
          <h1>{state.data.call.title}</h1>

          {state.data.programmes.length === 0 ? (
            <p>No programmes are available for this call yet.</p>
          ) : (
            <ul>
              {state.data.programmes.map((programme) => (
                <li key={programme.id}>
                  <a href={`/programmes/${programme.id}`}>
                    {programme.identifier} — {programme.title}
                  </a>
                </li>
              ))}
            </ul>
          )}
        </>
      )}
    </main>
  );
}
