import { AllEvent, LongEvent, ShortEvent } from "../static/types/Event";

export async function createEvent(
  token: string,
  name: string,
  description: string,
  category: string[],
  userId: string
): Promise<ShortEvent> {
  return await (
    await fetch(`${import.meta.env.VITE_PUBLIC_BACKEND_URL}/event/post`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        name: name,
        description: description,
        category: category,
        user_id: userId
      }),
    })
  ).json();
}

export async function getEventById(token: string, eventId: string): Promise<LongEvent> {
  return await (await fetch(`${import.meta.env.VITE_PUBLIC_BACKEND_URL}/event/get?event_id=${eventId}`, {
    headers: {
      Authorization: `Bearer ${token}`,
    }
  })).json()
}

export async function addUsersToEvent(
  token: string,
  eventId: string,
  names: string[],
  phones: (string | null)[]
) {
  return await (
    await fetch(`${import.meta.env.VITE_PUBLIC_BACKEND_URL}/event/add_user`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        event_id: eventId,
        names: names,
        phones: phones,
      }),
    })
  ).json();
}

export async function getAllEvents(token: string, userId: string): Promise<AllEvent[]> {
  return await (
    await fetch(
      `${
        import.meta.env.VITE_PUBLIC_BACKEND_URL
      }/event/get_all?user_id=${userId}`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    )
  ).json();
}

