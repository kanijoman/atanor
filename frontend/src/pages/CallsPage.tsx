import { type Call, fetchJson } from "../api";
import { useApi } from "../useApi";

export function CallsPage() {
  const state = useApi("calls", (signal) => fetchJson<Call[]>("/api/calls", signal));

  return (
    <main>
      <h1>Calls</h1>

      {state.status === "loading" && <p>Loading calls…</p>}

      {state.status === "error" && <p>Unable to load calls.</p>}

      {state.status === "ready" && state.data.length === 0 && <p>No calls are available yet.</p>}

      {state.status === "ready" && state.data.length > 0 && (
        <ul>
          {state.data.map((call) => (
            <li key={call.id}>
              <a href={`/calls/${call.id}`}>{call.title}</a>
            </li>
          ))}
        </ul>
      )}
    </main>
  );
}
