import styles from "./Create.module.scss";
import { Layout } from "../../components/Layout/Layout";
import { useCookies } from "react-cookie";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Member } from "../../static/types/Member";
import { generateInviteLink } from "../../utils/inviteLink";
import { addUsersToEvent, createEvent as createEventOnServer } from "../../utils/events";
// import { getCatImage } from "../../utils/cats";
// import loadingImg from "../../static/images/loading.svg";

export function Create() {
  const navigate = useNavigate();

  const [cookies] = useCookies(["IIWI_USERID", "IIWI_TOKEN"]);

  const [currentStage, setCurrentStage] = useState<0 | 1>(0);

  // const [catUrl, setCatUrl] = useState<string | null>(null);

  const [eventName, setEventName] = useState<string>("");
  const [eventDescription, setEventDescription] = useState<string>("");

  const [members, setMembers] = useState<Member[]>([]);
  const [categories, setCategories] = useState<string[]>([]);

  const [currentName, setCurrentName] = useState<string>("");
  const [currentPhone, setCurrentPhone] = useState<string>("");
  const [currentCategory, setCurrentCategory] = useState<string>("");

  const [createMemberError, setCreateMemberError] = useState<boolean>(false);
  const [createCategoryError, setCreateCategoryError] =
    useState<boolean>(false);

  const [createEventError, setCreateEventError] = useState<boolean>(false);
  const [createEventMembersError, setCreateEventMembersError] =
    useState<boolean>(false);

  const [eventId, setEventId] = useState<string | null>(null);

  useEffect(() => {
    if (!Boolean(cookies.IIWI_USERID)) {
      navigate("/login");
    }
  }, []);

  // useEffect(() => {
  //   getCatImage()
  //     .then((catImage) => {
  //       setCatUrl(catImage.url);
  //     })
  //     .catch((err) => {
  //       console.log(err);
  //     });
  // }, []);

  function createMember(name: string, phone: string) {
    if (!members.map((member) => member.name).includes(name) && name !== "") {
      setCreateMemberError(false);
      setMembers((members) => {
        return [{ name: name, phone: phone === "" ? null : phone }, ...members];
      });
      setCurrentName("");
      setCurrentPhone("");
    } else {
      setCreateMemberError(true);
    }
  }

  function removeMember(name: string) {
    setMembers((members) => members.filter((member) => member.name !== name));
  }

  function createCategory(name: string) {
    if (!categories.includes(name) && name !== "") {
      setCreateCategoryError(false);
      setCategories((categories) => {
        return [name, ...categories];
      });
      setCurrentCategory("");
    } else {
      setCreateCategoryError(true);
    }
  }

  function removeCategory(name: string) {
    setCategories((categories) =>
      categories.filter((category) => category !== name)
    );
  }

  function createEvent(
    eventName: string,
    eventDescription: string,
    categories: string[]
  ) {
    if (eventName !== "" && eventDescription !== "" && categories.length > 0) {
      setCreateEventError(false);
      createEventOnServer(cookies.IIWI_TOKEN, eventName, eventDescription, categories, cookies.IIWI_USERID)
        .then((event) => {
          setEventId(event.id);
          setCurrentStage(1);
        })
        .catch((err) => {
          console.log(err);
        });
    } else {
      setCreateEventError(true);
    }
  }

  function createEventMembers(members: Member[]) {
    if (eventName !== "" && eventDescription !== "" && members.length > 0) {
      setCreateEventMembersError(false);
      addUsersToEvent(cookies.IIWI_TOKEN, eventId ?? "", members.map(member => member.name), members.map(member => member.phone))
      .then(() => {
        navigate(`/events`);
      })
      .catch(err => {
        console.log(err);
      })
    } else {
      setCreateEventMembersError(true);
    }
  }

  return (
    <Layout>
      {currentStage === 0 ? (
        <section className={styles.create}>
          <header className={styles.header}>Создать событие</header>
          <div className={styles.block}>
            <input
              type="text"
              className={styles.input}
              placeholder="Введите название..."
              defaultValue={eventName}
              onChange={(evt) => setEventName(evt.target.value)}
            />
          </div>
          <div className={styles.block}>
            <input
              type="text"
              className={styles.input}
              placeholder="Введите описание..."
              defaultValue={eventDescription}
              onChange={(evt) => setEventDescription(evt.target.value)}
            />
          </div>
          <span className={styles.subheader}>Создать название трат</span>
          <div className={styles.block}>
            <div className={styles.column}>Название траты</div>
          </div>
          <div className={styles.block}>
            <input
              type="text"
              className={styles.block_input}
              placeholder="Название траты"
              onChange={(evt) => setCurrentCategory(evt.target.value)}
              value={currentCategory}
            />
            <button
              className={styles.block_btn}
              onClick={() => createCategory(currentCategory)}
            >
              +
            </button>
            <span className={styles.error}>
              {" "}
              {createCategoryError
                ? " (пожалуйста, введите корректное название траты)"
                : ""}
            </span>
          </div>
          {categories.length > 0 ? (
            <>
              <span className={styles.subheader}>Добавленные траты</span>
              <ul className={styles.list}>
                {categories.map((category, index) => (
                  <li className={styles.block} key={index}>
                    <div className={styles.member}>{category}</div>
                    <button
                      className={styles.block_btn}
                      onClick={() => removeCategory(category)}
                    >
                      -
                    </button>
                  </li>
                ))}
              </ul>
            </>
          ) : (
            ""
          )}
          <div className={styles.block}>
            <button
              className={styles.btn + " " + styles.btn_next}
              onClick={() =>
                createEvent(eventName, eventDescription, categories)
              }
            >
              Следующий шаг
            </button>
            {createEventError ? (
              <span className={styles.error}>
                Проверьте валидность введенных данных (имя, описание, траты)
              </span>
            ) : (
              ""
            )}
          </div>
        </section>
      ) : (
        ""
      )}
      {currentStage === 1 ? (
        <section className={styles.users}>
          <span className={styles.subheader}>Создать участников </span>
          <div className={styles.block}>
            <div className={styles.column}>Имя</div>
          </div>
          <div className={styles.block}>
            <input
              type="text"
              className={styles.block_input}
              placeholder="Имя"
              onChange={(evt) => setCurrentName(evt.target.value)}
              value={currentName}
              required
            />
            {currentName !== "" ? (
              <input
                type="text"
                className={styles.block_input}
                placeholder="Номер телефона"
                onChange={(evt) => setCurrentPhone(evt.target.value)}
              />
            ) : (
              ""
            )}
            <button
              className={styles.block_btn}
              onClick={() => createMember(currentName, currentPhone ?? "")}
            >
              +
            </button>
            <span className={styles.error}>
              {createMemberError
                ? "Имя введено неправильно, попробуйте еще раз"
                : ""}
            </span>
          </div>
          {members.length > 0 ? (
            <>
              <span className={styles.subheader}>Созданные участники</span>
              <ul className={styles.list}>
                {members.map((member, index) => (
                  <li className={styles.block} key={index}>
                    <div className={styles.member}>{member.name}</div>
                    <div className={styles.member}>
                      {member.phone ? member.phone : "Без телефона"}
                    </div>
                    <button
                      className={styles.link_btn}
                      onClick={() => removeMember(member.name)}
                    >
                      Скопировать ссылку
                    </button>
                    <button
                      className={styles.block_btn}
                      onClick={() => {
                        if (eventId) {
                          generateInviteLink(cookies.IIWI_TOKEN, eventId, member.name)
                            .then((inviteLink) => {
                              alert(inviteLink);
                            })
                            .catch((err) => {
                              console.log(err);
                            });
                        }
                      }}
                    >
                      -
                    </button>
                  </li>
                ))}
              </ul>
            </>
          ) : (
            ""
          )}
          <div className={styles.block}>
            <button
              className={styles.btn + " " + styles.back_btn}
              onClick={() => setCurrentStage(0)}
            >
              Назад
            </button>
            <button
              className={styles.btn}
              onClick={() => createEventMembers(members)}
            >
              Создать!
            </button>
            {createEventMembersError ? (
              <span className={styles.hint}>Добавьте пользователей</span>
            ) : (
              ""
            )}
          </div>
        </section>
      ) : (
        ""
      )}
      {/* <img src={catUrl ? catUrl : loadingImg} alt="" /> */}
    </Layout>
  );
}
