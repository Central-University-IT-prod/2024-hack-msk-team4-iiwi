import { MoneyStatus } from "../static/types/MoneyStatus";

interface GetStatusResponse {
  debter_id: string;
  status: MoneyStatus;
}

export async function getStatus(
  token: string,
  debterId: string
): Promise<GetStatusResponse> {
  return await (
    await fetch(
      `${
        import.meta.env.VITE_PUBLIC_BACKEND_URL
      }/status/get?debter_id=${debterId}`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    )
  ).json();
}

export async function setStatus(token: string, debterId: string, status: MoneyStatus) {
  return await (
    await fetch(`${import.meta.env.VITE_PUBLIC_BACKEND_URL}/status/set`, {
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({
        debter_id: debterId,
        status: status,
      }),
    })
  ).json();
}
