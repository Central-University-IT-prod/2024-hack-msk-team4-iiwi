import styles from "./Events.module.scss";
import { Layout } from "../../components/Layout/Layout";
import { useCookies } from "react-cookie";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { EventCard } from "../../components/EventCard/EventCard";
import { AllEvent } from '../../static/types/Event';
import { getAllEvents } from '../../utils/events';

export function Events() {
  const navigate = useNavigate();

  const [cookies] = useCookies(["IIWI_USERID", "IIWI_TOKEN"]);

  const [events, setEvents] = useState<AllEvent[]>([]);

  useEffect(() => {
    if (!Boolean(cookies.IIWI_USERID)) {
      navigate("/login");
    }
  }, []);

  useEffect(() => {
    getAllEvents(cookies.IIWI_TOKEN, cookies.IIWI_USERID)
    .then(events => {
      setEvents(events);
    })
    .catch(err => {
      console.log(err);
    })
  }, []);

  return (
    <Layout>
      <header className={styles.header}>Ваши события</header>
      <section className={styles.events}>
        {
          events.map((event, index) => (
            <EventCard event={event} key={index} />
          ))
        }
      </section>
    </Layout>
  );
}
