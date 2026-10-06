import { useEffect, useState } from "react";

type ApiState<T> =
  | { status: "loading" }
  | { status: "error"; error: unknown }
  | { status: "ready"; data: T };

/**
 * Runs `load` whenever `key` changes and exposes loading/error/ready state.
 * Stale responses are discarded: the previous request is aborted when `key`
 * changes or the component unmounts.
 */
export function useApi<T>(
  key: string,
  load: (signal: AbortSignal) => Promise<T>,
): ApiState<T> {
  const [state, setState] = useState<ApiState<T>>({ status: "loading" });

  useEffect(() => {
    const controller = new AbortController();
    setState({ status: "loading" });

    load(controller.signal)
      .then((data) => setState({ status: "ready", data }))
      .catch((error: unknown) => {
        if (!controller.signal.aborted) {
          setState({ status: "error", error });
        }
      });

    return () => controller.abort();
    // `load` is derived from `key`; re-running on identity changes would loop.
  }, [key]);

  return state;
}
