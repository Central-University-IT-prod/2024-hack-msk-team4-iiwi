import styles from "./EventPage.module.scss";
import { Layout } from "../../components/Layout/Layout";
import { useCookies } from "react-cookie";
import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { CreateDebter, Debter } from "../../static/types/Debter";
import { createDebter, getAllDebters, updateDebter } from "../../utils/debter";
import { Chart } from "../../components/Chart/Chart";
import { setStatus } from "../../utils/status";
import { getEventById } from "../../utils/events";
import { LongEvent } from "../../static/types/Event";

export function EventPage() {
  const navigate = useNavigate();

  const [cookies] = useCookies(["IIWI_USERID", "IIWI_TOKEN"]);

  const { eventId } = useParams();

  const [debters, setDebters] = useState<Debter[]>([]);

  const [debtersVisible] = useState<boolean>(false);

  const [isWallet, setIsWallet] = useState<boolean>(false);
  const [currentWallet, setCurrentWallet] = useState<string>("");

  const [newDebters, setNewDebters] = useState<CreateDebter[]>([]);
  const [newDebter, setNewDebter] = useState<CreateDebter>({
    category_id: "",
    user_id: "",
    debter: true,
    paid: 0,
    auto: true,
    members: [],
  });

  const [event, setEvent] = useState<LongEvent | null>(null);

  useEffect(() => {
    if (!Boolean(cookies.IIWI_USERID)) {
      navigate("/login");
    }
  }, []);

  useEffect(() => {
    getEventById(cookies.IIWI_TOKEN, eventId ?? "")
      .then((event) => {
        getAllDebters(cookies.IIWI_TOKEN, eventId ?? "")
          .then((debters) => {
            setDebters(debters);
            setEvent(event);
            console.log(debters);
          })
          .catch((err) => {
            console.log(err);
          });
      })
      .catch((err) => {
        console.log(err);
      });
  }, []);

  function addDebter(newDebter: CreateDebter) {
    setNewDebters((newDebters) => {
      return [newDebter, ...newDebters];
    });
  }

  useEffect(() => {
    if (event) {
      if (newDebter.auto) {
        setNewDebter((newDebter) => {
          return {
            ...newDebter,
            members: [],
          };
        });
      } else {
        setNewDebter((newDebter) => {
          return {
            ...newDebter,
            members: event?.users.map((user) => {
              return {
                user_id: user.user_id,
                name: user.name,
                debt: 0,
                status: 0,
              };
            }),
          };
        });
      }
    }
  }, [newDebter.auto]);

  return (
    <Layout>
      {event ? (
        <>
          <header className={styles.header}>{event.name}</header>
          <div className={styles.subheader}>{event.description}</div>
          {debters.length > 0 ? (
            <>
              <span>{debters[0].lender.name}</span>
              <span>
                {debters[0].debters.map((debter) => (
                  <span>{debter.name}</span>
                ))}
              </span>
            </>
          ) : (
            ""
          )}
          <Chart />
          {debters[0].lender.user_id === cookies.IIWI_USERID ? (
            <div className={styles.cont}>
              <div className={styles.block}>
                <select
                  className={styles.input}
                  defaultValue={event.categories[0].category_id}
                  onChange={(evt) =>
                    setNewDebter((newDebter) => {
                      return {
                        ...newDebter,
                        category_id: evt.target.value,
                      };
                    })
                  }
                >
                  {event.categories.map((category) => (
                    <option value={category.category_id}>
                      {category.name}
                    </option>
                  ))}
                </select>
                {newDebter.debter ? (
                  <select
                    className={styles.input}
                    defaultValue={
                      event.users.filter(
                        (user) => user.user_id !== debters[0].lender.user_id
                      )[0].user_id
                    }
                    onChange={(evt) =>
                      setNewDebter((newDebter) => {
                        return {
                          ...newDebter,
                          user_id: evt.target.value,
                        };
                      })
                    }
                  >
                    {event.users
                      .filter(
                        (user) => user.user_id !== debters[0].lender.user_id
                      )
                      .map((debter) => (
                        <option value={debter.user_id}>{debter.name}</option>
                      ))}
                  </select>
                ) : (
                  ""
                )}
                <input
                  type="checkbox"
                  id="isDebter"
                  defaultChecked={true}
                  onChange={(evt) =>
                    setNewDebter((newDebter) => {
                      return {
                        ...newDebter,
                        debter: evt.target.checked,
                      };
                    })
                  }
                />
                <label htmlFor="isDebter">Должник</label>
                <div className={styles.block}>
                  {!newDebter.debter ? (
                    <input
                      type="number"
                      className={styles.input}
                      onChange={(evt) =>
                        setNewDebter((newDebter) => {
                          return {
                            ...newDebter,
                            paid: Number(evt.target.value),
                          };
                        })
                      }
                    />
                  ) : (
                    <div className={styles.block}>
                      <input
                        type="checkbox"
                        id="isAuto"
                        defaultChecked={true}
                        onChange={(evt) =>
                          setNewDebter((newDebter) => {
                            return {
                              ...newDebter,
                              auto: evt.target.checked,
                            };
                          })
                        }
                      />
                      <label htmlFor="isAuto">Автоматический расчет</label>
                      {!newDebter.auto ? (
                        <div className={styles.block}>
                          <span>Расчет вручную</span>
                          <div className={styles.block}>
                            {newDebter.members
                              .filter(
                                (member) =>
                                  member.user_id !== debters[0].lender.user_id
                              )
                              .map((member) => (
                                <div className={styles.block}>
                                  <span>{member.name}</span>
                                  <input
                                    type="number"
                                    className={styles.input}
                                    defaultValue={member.debt}
                                    onChange={(evt) => {
                                      setNewDebter((newDebter) => {
                                        return {
                                          ...newDebter,
                                          members: newDebter.members.map(
                                            (imember) => {
                                              if (
                                                member.user_id ===
                                                imember.user_id
                                              ) {
                                                return {
                                                  ...member,
                                                  debt: Number(
                                                    evt.target.value
                                                  ),
                                                };
                                              }
                                              return member;
                                            }
                                          ),
                                        };
                                      });
                                    }}
                                  />
                                </div>
                              ))}
                          </div>
                        </div>
                      ) : (
                        ""
                      )}
                    </div>
                  )}
                  <button
                    className={styles.btn}
                    onClick={() => addDebter(newDebter)}
                  >
                    Сохранить
                  </button>
                </div>
              </div>
              <div className={styles.block}>
                {newDebters.map((newDebter) =>
                  newDebter.debter ? (
                    <span>
                      {newDebter.user_id} - должник в категории{" "}
                      {newDebter.category_id}
                    </span>
                  ) : (
                    <span>
                      {debters[0].lender.name} Заплатил {newDebter.paid} рублей
                    </span>
                  )
                )}
              </div>
              <div className={styles.block}>
                <button
                  className={styles.btn}
                  onClick={() => createDebter(cookies.IIWI_TOKEN, newDebters)}
                >
                  Создать должников
                </button>
              </div>
            </div>
          ) : (
            ""
          )}

          {/* {debters[0].lender.user_id === cookies.IIWI_USERID ? (
            <div className={styles.block}>
              <input
                type="checkbox"
                id="all_debters"
                onChange={(evt) => setDebtersVisible(evt.target.checked)}
              />
              <label htmlFor="all_debters">
                Показать долги всех участников
              </label>
            </div>
          ) : (
            ""
          )} */}
          <div className={styles.block}>
            {debtersVisible &&
            debters[0].lender.user_id === cookies.IIWI_USERID ? (
              <div className={styles.debters}>
                {debters[0].members.length > 0
                  ? debters[0].members.map((userDebt, index) => (
                      <div className={styles.debter} key={index}>
                        <span className={styles.debter_field}>
                          {userDebt.name}
                        </span>
                        <span className={styles.debter_field}>
                          должен отдать
                        </span>
                        <span className={styles.debter_field}>
                          {debters[0].lender.name}
                        </span>
                        <span className={styles.debter_field}>
                          {userDebt.debt}
                        </span>
                        {debters[0].lender.user_id === cookies.IIWI_USERID ? (
                          <span className={styles.debter_field}>
                            {userDebt.status === 0 ? (
                              "Не отправлено"
                            ) : userDebt.status === 1 ? (
                              <>
                                <span>Деньги отправлены</span>
                                <button
                                  className={styles.btn}
                                  onClick={() =>
                                    setStatus(
                                      cookies.IIWI_TOKEN,
                                      userDebt.user_id,
                                      0
                                    )
                                  }
                                >
                                  Отклонить перевод
                                </button>
                                <button
                                  className={styles.btn}
                                  onClick={() =>
                                    setStatus(
                                      cookies.IIWI_TOKEN,
                                      userDebt.user_id,
                                      2
                                    )
                                  }
                                >
                                  Подтвердить перевод
                                </button>
                              </>
                            ) : userDebt.status === 2 ? (
                              "Деньги получены"
                            ) : (
                              ""
                            )}
                          </span>
                        ) : (
                          ""
                        )}
                      </div>
                    ))
                  : ""}
              </div>
            ) : (
              ""
            )}
            {debters[0].members.filter(
              (debter) => debter.debt === cookies.IIWI_USERID
            ).length > 0 &&
            debters[0].lender.user_id !== cookies.IIWI_USERID ? (
              <>
                <span className={styles.subheader}>Мои долги</span>
                <div className={styles.debters}>
                  {debters[0].members
                    .filter((debter) => debter.user_id === cookies.IIWI_USERID)
                    .map((userDebt, index) => (
                      <div className={styles.debter} key={index}>
                        <span className={styles.debter_field}>
                          {userDebt.name}
                        </span>
                        <span className={styles.debter_field}>
                          должен отдать
                        </span>
                        <span className={styles.debter_field}>
                          {debters[0].lender.name}
                        </span>
                        <span className={styles.debter_field}>
                          {userDebt.debt}
                        </span>
                      </div>
                    ))}
                </div>
              </>
            ) : (
              ""
            )}
            {debters.length > 0 && debters[0].lender_wallet ? (
              debters[0].lender.user_id === cookies.IIWI_USERID ? (
                <div className={styles.block}>
                  <span className={styles.block}>
                    Вам должны {debters[0].debt} рублей.
                  </span>
                </div>
              ) : (
                <span className={styles.block}>
                  Реквизиты: {debters[0].lender_wallet}
                </span>
              )
            ) : (
              ""
            )}
            {debters[0].lender.user_id === cookies.IIWI_USERID &&
            debters[0].wallet ? (
              <>
                <input
                  type="checkbox"
                  id="isCrypto"
                  defaultChecked={false}
                  onChange={(evt) => setIsWallet(evt.target.checked)}
                />
                <label htmlFor="isCrypto">Крипто-кошелек</label>
                <span className={styles.block}>Ввести номер кошелька</span>
                <input
                  type="text"
                  className={styles.input}
                  onChange={(evt) => setCurrentWallet(evt.target.value)}
                />
                <button
                  className={styles.btn}
                  onClick={() => {
                    if (currentWallet !== "") {
                      updateDebter(
                        cookies.IIWI_TOKEN,
                        debters[0].lender.user_id,
                        currentWallet,
                        isWallet
                      )
                        .then(() => {
                          navigate(0);
                        })
                        .catch((err) => {
                          console.log(err);
                        });
                    }
                  }}
                >
                  Сохранить
                </button>
              </>
            ) : debters[0].wallet ? (
              <div className={styles.block}>
                <span className={styles.block}>
                  Реквизиты криптокошелька: {debters[0].lender_wallet}
                </span>
                {debters[0].members.find(
                  (member) => member.user_id === cookies.IIWI_USERID
                ) ? (
                  <div className={styles.block}>
                    <span>
                      Вы должны:{" "}
                      {debters[0].members.find(
                        (member) => member.user_id === cookies.IIWI_USERID
                      )?.debt ?? 0}{" "}
                      ₽
                    </span>
                    {debters[0].members.find(
                      (member) => member.user_id === cookies.IIWI_USERID
                    )?.status === 0 ? (
                      <button
                        className={styles.btn}
                        onClick={() =>
                          setStatus(cookies.IIWI_TOKEN, cookies.IIWI_USERID, 1)
                        }
                      >
                        Отправить подтверждение о переводе
                      </button>
                    ) : debters[0].members.find(
                        (member) => member.user_id === cookies.IIWI_USERID
                      )?.status === 1 ? (
                      <span>Деньги отправлены</span>
                    ) : debters[0].members.find(
                        (member) => member.user_id === cookies.IIWI_USERID
                      )?.status === 2 ? (
                      <span>Деньги получены</span>
                    ) : (
                      ""
                    )}
                  </div>
                ) : (
                  ""
                )}
              </div>
            ) : (
              ""
            )}
          </div>
        </>
      ) : (
        ""
      )}
    </Layout>
  );
}
