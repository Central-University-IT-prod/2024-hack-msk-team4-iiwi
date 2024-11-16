interface Token {
  access_token: string;
  token_type: string;
}


export function auth(username: string, password: string): Promise<Token> {
  return new Promise((resolve, reject) => {
    fetch(`${import.meta.env.VITE_PUBLIC_BACKEND_URL}/token/new`, {
      method: 'POST',
      headers:{
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: new URLSearchParams({
        username: username,
        password: password
      })
    })
    .then(res => res.json())
    .then(data => {
      resolve(data);
    })
    .catch(err => {
      reject(err);
    })
  })
}