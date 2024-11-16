import { SuperCuttedUser } from "./User";

export interface LongEvent {
  name: string;
  description: string;
  completed: boolean;
  users: SuperCuttedUser[];
  categories: {name: string, category_id: string}[];
}

export interface ShortEvent {
  id: string;
  name: string;
  description: string;
  categories: {
    category_id: string;
    name: string;
  }[];
}

export interface AllEvent {
  order_id: string;
  name: string;
  description: string;
  categories: {
    category_id: string;
    name: string;
  }[];
}
