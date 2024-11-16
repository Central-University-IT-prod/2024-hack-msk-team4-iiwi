import { IdCollection } from './IdCollection';
import { LongEvent } from './Event';
import { Category } from './Category';

export interface User {
  id: string;
  name: string;
  category: Category[];
  event: LongEvent;
}

export interface CuttedUser {
  _id: string;
  name: string;
  category: Category[];
  event: IdCollection[];
}

export interface SuperCuttedUser {
  user_id: string;
  name: string;
}