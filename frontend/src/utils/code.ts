export async function checkCode(token: string, code: number, phone: string): Promise<{user_id: string}> {
  const response = await fetch(`${import.meta.env.VITE_PUBLIC_BACKEND_URL}/code/test/check`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({
      code: code,
      phone: phone
    })
  });

  if (response.ok) {
    return await response.json();
  } else {
    return {user_id: ""}
  }
}