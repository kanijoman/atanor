import { useEffect, useRef, useState } from "react";

type ApiState<T> =
  { status: "loading" } | { status: "error"; error: unknown } | { status: "ready"; data: T };

type Settled<T> = { key: string } & Exclude<ApiState<T>, { status: "loading" }>;

/**
 * Runs `load` whenever `key` changes and exposes loading/error/ready state.
 * Loading is derived (no result for the current key yet), and stale responses
 * are discarded: the previous request is aborted when `key` changes or the
 * component unmounts.
 */
export function useApi<T>(key: string, load: (signal: AbortSignal) => Promise<T>): ApiState<T> {
  const [settled, setSettled] = useState<Settled<T> | null>(null);
  const loadRef = useRef(load);

  useEffect(() => {
    loadRef.current = load;
  });

  useEffect(() => {
    const controller = new AbortController();

    loadRef
      .current(controller.signal)
      .then((data) => setSettled({ key, status: "ready", data }))
      .catch((error: unknown) => {
        if (!controller.signal.aborted) {
          setSettled({ key, status: "error", error });
        }
      });

    return () => controller.abort();
  }, [key]);

  return settled?.key === key ? settled : { status: "loading" };
}
