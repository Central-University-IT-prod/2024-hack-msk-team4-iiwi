interface GenerateResponse {
  link: string;
}

export async function generateInviteLink(
  token: string,
  eventId: string,
  name: string
): Promise<GenerateResponse> {
  return await (
    await fetch(
      `${import.meta.env.VITE_PUBLIC_BACKEND_URL}/invite_link/generate`,
      {
        method: "POST",
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({
          event_id: eventId,
          name: name,
        }),
      }
    )
  ).json();
}
