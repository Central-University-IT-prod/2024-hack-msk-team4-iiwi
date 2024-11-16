import styles from "./Home.module.scss";
import { Layout } from "../../components/Layout/Layout";
import { Link } from "react-router-dom";

export function Home() {
  return (
    <Layout>
      <section className={styles.landing}>
        <header className={styles.landing_header}>iiwi</header>
        <span className={styles.landing_description}>
          сервис для разделения счета
        </span>
        <div className={styles.block}>
          <Link to="/events" className={styles.btn}>
            Начать использовать
          </Link>
        </div>
      </section>
    </Layout>
  );
}
