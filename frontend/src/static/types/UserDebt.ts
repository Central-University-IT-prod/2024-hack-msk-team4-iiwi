import { MoneyStatus } from './MoneyStatus';

export interface UserDebt {
  user_id: string;
  name: string;
  debt: number;
  status: MoneyStatus;
}