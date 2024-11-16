import { useEffect, useState } from "react";
import styles from "./PayBill.module.scss";
import { useParams } from "react-router-dom";
import { getAllDebters } from "../../utils/debter";
import { useCookies } from "react-cookie";
import { Debter } from "../../static/types/Debter";
import { getStatus, setStatus } from "../../utils/status";
import { MoneyStatus } from "../../static/types/MoneyStatus";

export function PayBill() {
  const [cookies] = useCookies(["IIWI_USERID", "IIWI_TOKEN"]);

  const { eventId, debterId } = useParams();

  const [debters, setDebters] = useState<Debter[]>([]);

  const [currentStatus, setCurrentStatus] = useState<MoneyStatus | -1>(-1);

  useEffect(() => {
    getAllDebters(cookies.IIWI_TOKEN, eventId ?? "")
      .then((debters) => {
        setDebters(debters);
        getStatus(cookies.IIWI_TOKEN, debterId ?? "")
          .then((status) => {
            setCurrentStatus(status.status);
          })
          .catch((err) => {
            console.log(err);
          });
      })
      .catch((err) => {
        console.log(err);
      });
  }, []);

  return currentStatus !== -1 && debters.length > 0 ? (
    <section className={styles.pay}>
      <header className={styles.header}>Оплатить без регистрации</header>
      <div className={styles.block}>
        Вам необходимо отправить на кошелек {debters[0].lender_wallet}{" "}
        {debters[0].members.find((member) => member.user_id === debterId)?.debt}{" "}
        рублей
      </div>
      <div className={styles.block}>
        {currentStatus === 0 ? (
          <button
            className={styles.btn}
            onClick={() => setStatus(cookies.IIWI_TOKEN, debterId ?? "", 1)}
          >
            Уведомить об оплате
          </button>
        ) : currentStatus === 1 ? (
          <span>Деньги отправлены</span>
        ) : currentStatus === 2 ? (
          <span>Перевод подтвержден</span>
        ) : (
          ""
        )}
      </div>
    </section>
  ) : (
    ""
  );
}
