import { CreateDebter, Debter } from "../static/types/Debter";

export async function getAllDebters(token: string, eventId: string): Promise<Debter[]> {
  return await (
    await fetch(
      `${
        import.meta.env.VITE_PUBLIC_BACKEND_URL
      }/debter/get_all?event_id=${eventId}`,
      {
        headers:
        {
          Authorization: `Bearer ${token}`
        }
      }
    )
  ).json();
}

export async function updateDebter(token: string, lenderId: string, lenderWallet: string, wallet: boolean) {
  return await (
    await fetch(
      `${
        import.meta.env.VITE_PUBLIC_BACKEND_URL
      }/debter/update`,
      {
        method: 'PATCH',
        headers:
        {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          lender_id: lenderId,
          lender_wallet: lenderWallet,
          wallet: wallet
        })
      }
    )
  ).json();
}

export async function createDebter(token: string, debter: CreateDebter[]) {
  return await (
    await fetch(
      `${
        import.meta.env.VITE_PUBLIC_BACKEND_URL
      }/debter/create`,
      {
        method: 'POST',
        headers:
        {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(debter)
      }
    )
  ).json();
}