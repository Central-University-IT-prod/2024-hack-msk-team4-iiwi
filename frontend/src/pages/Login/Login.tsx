import styles from "./Login.module.scss";
import { Layout } from "../../components/Layout/Layout";
import { useEffect, useState } from "react";
import { useCookies } from "react-cookie";
import { numberRegex } from "../../regexes/number";
import keyIcon from "../../static/icons/key.svg";
import checkIcon from "../../static/icons/check.svg";
import repeatIcon from "../../static/icons/repeat.svg";
import { useNavigate } from "react-router-dom";
import { checkCode } from '../../utils/code';

export function Login() {
  const navigate = useNavigate();

  const [cookies, setCookie] = useCookies(["IIWI_USERID", "IIWI_TOKEN"]);

  const [currentStage, setCurrentStage] = useState<0 | 1>(0);

  const [phone, setPhone] = useState<string>("");
  const [code, setCode] = useState<string>("");

  const [phoneError, setPhoneError] = useState<boolean>(false);
  const [codeError, setCodeError] = useState<boolean>(false);

  const [isRepeatBlocked, setIsRepeatBlocked] = useState<boolean>(false);

  function sendMessage(phone: string) {
    // send sms message to user
    if (numberRegex.test(phone) && phone.length === 10) {
      setCurrentStage(1);
    } else {
      setPhoneError(true);
    }
  }

  function sendCode(code: number, phone: string) {
    if (numberRegex.test(String(code)) && String(code).length === 6) {
      checkCode(cookies.IIWI_TOKEN, code, phone)
      .then(userId => {
        if (userId.user_id !== "") {
          // auth user
          setCookie("IIWI_USERID", userId.user_id);
          navigate("/events");
        } else {
          setCodeError(true);
        }
      })
      .catch((err) => {
        console.log(err);
        setCodeError(true);
      })
    } else {
      setCodeError(true);
    }
  }

  useEffect(() => {
    if (Boolean(cookies.IIWI_USERID)) {
      // check in backend
      navigate("/events");
    }
  }, []);

  useEffect(() => {
    if (phoneError) {
      setPhoneError(false);
    }
  }, [phone]);

  function repeat(phone: string) {
    if (numberRegex.test(phone) && phone.length === 10 && currentStage === 1 && !isRepeatBlocked) {
      setIsRepeatBlocked(true);
      const timeout = setTimeout(() => {
        setIsRepeatBlocked(false);
      }, 40000);

      return () => clearTimeout(timeout);
    }
  }

  return (
    <Layout>
      <section className={styles.form}>
        {currentStage === 0 ? (
          <>
            <div className={styles.block}>
              <header className={styles.header}>Авторизация</header>
              <span
                className={
                  phoneError
                    ? styles.hint + " " + styles.hint_error
                    : styles.hint
                }
              >
                {phoneError
                  ? "Номер телефона неккоректен"
                  : "Введите номер телефона для входа в систему"}
              </span>
            </div>
            <div className={styles.block}>
              <div className={styles.code}>+7</div>
              <input
                type="number"
                className={styles.input}
                onChange={(evt) => setPhone(evt.target.value)}
                maxLength={10}
              />
            </div>
            <div className={styles.block}>
              <button className={styles.btn} onClick={() => sendMessage(phone)}>
                <img src={keyIcon} alt="" className={styles.btn_icon} />
                <span className={styles.btn_text}>Вход по номеру телефона</span>
              </button>
            </div>
          </>
        ) : (
          ""
        )}
        {currentStage === 1 ? (
          <div className={styles.block}>
            <div className={styles.block}>
              <div className={styles.header}>Введите код</div>
              <span
                className={
                  codeError
                    ? styles.hint + " " + styles.hint_error
                    : styles.hint
                }
              >
                {codeError
                  ? "Код неправильный"
                  : "Введите код, который пришел вам в SMS"}
              </span>
            </div>
            <div className={styles.block}>
              <input
                type="number"
                className={styles.input}
                onChange={(evt) => setCode(evt.target.value)}
              />
            </div>
            <div className={styles.block}>
              <button className={styles.btn}>
                <img src={checkIcon} alt="" className={styles.btn_icon} />
                <span
                  className={styles.btn_text}
                  onClick={() => sendCode(Number(code), `+7${phone}`)}
                >
                  Проверить код
                </span>
              </button>
              <button className={styles.btn} onClick={() => repeat(phone)} disabled={isRepeatBlocked}>
                <img src={repeatIcon} alt="" className={styles.btn_icon} />
                <span className={styles.btn_text}>Отправить еще раз</span>
              </button>
            </div>
          </div>
        ) : (
          ""
        )}
      </section>
    </Layout>
  );
}
