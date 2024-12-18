### JSON request for /pMessage.aspx/ListMessages

```json
{
    "what": "send",
    "muid": "",
    "track": "1",
    "UIDA": "",
    "Src": "",
    "DateFrom": "",
    "DateTo": "",
    "noUpdate": 1,
    "ID": "",
    "jtStartIndex": "0",
    "jtPageSize": "20",
    "jtSorting": "m_DT DESC",
}
```

- what - message type ["input", "output", "send", "delete"]
- muid - ID cообщения
- track - 1 - with track, 2 - without track
- UIDA - Отправитель
- Src - Тема сообщения
- noUpdate - idk
- ID - userLoginGS from cookie

### Cookie format

```json
[
    "_ym_d",
    "_ym_isad",
    "_ym_uid",
    "_ym_visorc",
    "ASP.NET_SessionId",
    "fullNameGS",
    "trueUserV",
    "userClientGS",
    "userLoginGS",
    "userNameGS",
]
```
