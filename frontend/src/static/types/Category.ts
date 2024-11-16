import { CuttedUser } from './User';

export interface Category {
  name: string;
  description: string;
  lenders_amount: number[];
  lenders: CuttedUser[];
  debters: CuttedUser[];
}