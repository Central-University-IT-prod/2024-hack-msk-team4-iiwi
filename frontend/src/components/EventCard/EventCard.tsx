import styles from "./EventCard.module.scss";
import arrowRightIcon from "../../static/icons/arrow-right.svg";
import { Link } from "react-router-dom";
import { AllEvent } from "../../static/types/Event";

export function EventCard({ event }: { event: AllEvent }) {
  return (
    <Link to={`/event/${event.order_id}`} className={styles.card}>
      <header className={styles.name}>{event.name}</header>
      <div className={styles.members}>
        <span className={styles.members_header}>Описание:</span>
        <span className={styles.members_names}>{event.description}</span>
      </div>
      <img src={arrowRightIcon} alt="" className={styles.icon} />
    </Link>
  );
}
