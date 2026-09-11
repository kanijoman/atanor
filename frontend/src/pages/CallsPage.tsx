import { useEffect, useState } from "react";

type Call = {
  id: string;
  title: string;
};

export function CallsPage() {
  const [calls, setCalls] = useState<Call[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    fetch("/api/calls")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Unable to load calls");
        }
        return response.json() as Promise<Call[]>;
      })
      .then(setCalls)
      .catch(() => setError(true))
      .finally(() => setLoading(false));
  }, []);

  return (
    <main>
      <h1>Calls</h1>

      {loading && <p>Loading calls…</p>}

      {!loading && error && <p>Unable to load calls.</p>}

      {!loading && !error && calls.length === 0 && (
        <p>No calls are available yet.</p>
      )}

      {!loading && !error && calls.length > 0 && (
        <ul>
          {calls.map((call) => (
            <li key={call.id}>
              <a href={`/calls/${call.id}`}>{call.title}</a>
            </li>
          ))}
        </ul>
      )}
    </main>
  );
}
