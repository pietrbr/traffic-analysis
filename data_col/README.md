# Data description

The scenario is emulated on Colosseum: scenario 12356.

## Session 4 (2022-09)

One test was performed on Colosseum:

- scenario: 12356
- bs: [5]
- uav: [1]
- ue: []

| N.  | CMD a port | TEL a port | CMD r port | TEL r port | File Name BS       | File Name UE         |
| --- | ---------- | ---------- | ---------- | ---------- | ------------------ | -------------------- |
| 1   | 44552      | 44554      | 52854      | 52856      | col_1uav_bs.pcapng | col_1uav_uav1.pcapng |

## Session 5 (2022-09)

Two tests were performed on Colosseum:

### Test 1

- scenario: 12356
- bs: [5]
- uav: [1, 2, 3]
- ue: []

| UAV IP address | CMD a port | TEL a port | CMD r port | TEL r port | File Name BS       | File Name UE         |
| -------------- | ---------- | ---------- | ---------- | ---------- | ------------------ | -------------------- |
| 172.16.0.8     | 54366      | 54372      | 54484      | 54486      | col_3uav_bs.pcapng | col_3uav_uav1.pcapng |
| 172.16.0.9     | 38114      | 38118      | 52300      | 52302      | col_3uav_bs.pcapng | col_3uav_uav2.pcapng |
| 172.16.0.10    | 32790      | 32792      | 58336      | 58338      | col_3uav_bs.pcapng | col_3uav_uav3.pcapng |

### Test 2

- scenario: 12356
- bs: [5]
- uav: [1]
- ue: [1, 2, 3]

| UAV IP address | CMD a port | TEL a port | CMD r port | TEL r port | File Name BS       | File Name UE         |
| -------------- | ---------- | ---------- | ---------- | ---------- | ------------------ | -------------------- |
| 172.16.0.8     | 60558      | 60568      | 57022      | 57024      | col_1uav3ue_bs.pcapng | col_1uav3ue_uav1.pcapng |
