import { SuperCuttedUser } from "./User";
import { UserDebt } from "./UserDebt";

export interface Debter {
  debters: SuperCuttedUser[];
  lender: SuperCuttedUser;
  debt: number;
  lender_wallet: string;
  wallet: boolean;
  members: UserDebt[];
}

export interface CreateDebter {
  category_id: string;
  user_id: string;
  debter: boolean;
  paid: number;
  auto: boolean;
  members: UserDebt[];
}
