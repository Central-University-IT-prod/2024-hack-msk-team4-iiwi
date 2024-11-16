import styles from "./Layout.module.scss";
import { ReactNode, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useCookies } from "react-cookie";
import logo from "../../static/icons/iiwi.svg";
import plusIcon from "../../static/icons/plus.svg";
import userIcon from "../../static/icons/user.svg";
import exitIcon from "../../static/icons/exit.svg";
import billIcon from '../../static/icons/bill.svg';
import { auth } from '../../utils/auth';

export function Layout({ children }: { children: ReactNode }) {
  const navigate = useNavigate();

  const [cookies, setCookie, removeCookie] = useCookies(["IIWI_USERID", "IIWI_TOKEN"]);

  useEffect(() => {
    auth(import.meta.env.VITE_PUBLIC_USERNAME, import.meta.env.VITE_PUBLIC_PASSWORD)
    .then(token => {
      setCookie("IIWI_TOKEN", token.access_token);
    })
    .catch(err => {
      console.log(err);
    })
  }, []);

  return (
    <div className={styles.wrapper}>
      <header className={styles.header}>
        <Link to="/">
          <img src={logo} alt="" className={styles.logo} />
        </Link>
        <nav className={styles.menu}>
          {Boolean(cookies.IIWI_USERID) ? (
            <>
              <Link to="/create" className={styles.btn}>
                <img src={plusIcon} alt="" className={styles.btn_icon} />
                <span className={styles.btn_text}>Создать событие</span>
              </Link>
              <Link to="/events" className={styles.btn}>
                <img src={billIcon} alt="" className={styles.btn_icon} />
                <span className={styles.btn_text}>Мои события</span>
              </Link>
            </>
          ) : (
            ""
          )}
          {!Boolean(cookies.IIWI_USERID) ? (
            <Link to="/login" className={styles.btn}>
              <img src={userIcon} alt="" className={styles.btn_icon} />
              <span className={styles.btn_text}>Войти</span>
            </Link>
          ) : (
            <button
              className={styles.btn}
              onClick={() => {
                removeCookie("IIWI_USERID");
                navigate(0);
              }}
            >
              <img src={exitIcon} alt="" className={styles.btn_icon} />
              <span className={styles.btn_text}>Выйти</span>
            </button>
          )}
        </nav>
      </header>
      <main className={styles.main}>{children}</main>
    </div>
  );
}
