import { CatInfo } from '../static/types/CatInfo';

export async function getCatImage() {
  const cat: CatInfo[] = await (await fetch(`https://api.thecatapi.com/v1/images/search`)).json();
  return cat[0];
}