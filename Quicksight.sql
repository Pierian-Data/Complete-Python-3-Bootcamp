select *,
    sum(department_revenue) over (partition by client_id, id, department) as revenue_cleaned
from (
        select Client_Name,
            Department_Name,
            Strategy_Name,
            Strategy_Status,
            Strategy_Type,
            Strategy_Date,
            Strategy_Created_at,
            Strategy_Updated_at,
            Strategy_Deleted_at,
            pillar_id,
            Pillar_Name,
            Records,
            monthly_gross_profit,
            total_gross_profit,
            id,
            tenant_id,
            client_id,
            audit_id,
            total_hours,
            hourly_rate,
            length,
            department,
            Service_Name,
            Task_Name,
            Task_Hours,
            case
                dates.Month
                When 'month1' THEN month1
                When 'month2' THEN month2
                When 'month3' THEN month3
                When 'month4' THEN month4
                When 'month5' THEN month5
                When 'month6' THEN month6
                When 'month7' THEN month7
                When 'month8' THEN month8
                When 'month9' THEN month9
                When 'month10' THEN month10
                When 'month11' THEN month11
                When 'month12' THEN month12
                When 'month13' THEN month13
                When 'month14' THEN month14
                When 'month15' THEN month15
                When 'month16' THEN month16
                When 'month17' THEN month17
                When 'month18' THEN month18
                When 'month19' THEN month19
                When 'month20' THEN month20
                When 'month21' THEN month21
                When 'month22' THEN month22
                When 'month23' THEN month23
                When 'month24' THEN month24
            end as Department_Revenue,
            case
                dates.Month
                When 'month1' THEN cast(
                    date_add(Strategy_Date, INTERVAL 0 MONTH) as date
                )
                When 'month2' THEN cast(
                    date_add(Strategy_Date, INTERVAL 1 MONTH) as date
                )
                When 'month3' THEN cast(
                    date_add(Strategy_Date, INTERVAL 2 MONTH) as date
                )
                When 'month4' THEN cast(
                    date_add(Strategy_Date, INTERVAL 3 MONTH) as date
                )
                When 'month5' THEN cast(
                    date_add(Strategy_Date, INTERVAL 4 MONTH) as date
                )
                When 'month6' THEN cast(
                    date_add(Strategy_Date, INTERVAL 5 MONTH) as date
                )
                When 'month7' THEN cast(
                    date_add(Strategy_Date, INTERVAL 6 MONTH) as date
                )
                When 'month8' THEN cast(
                    date_add(Strategy_Date, INTERVAL 7 MONTH) as date
                )
                When 'month9' THEN cast(
                    date_add(Strategy_Date, INTERVAL 8 MONTH) as date
                )
                When 'month10' THEN cast(
                    date_add(Strategy_Date, INTERVAL 9 MONTH) as date
                )
                When 'month11' THEN cast(
                    date_add(Strategy_Date, INTERVAL 10 MONTH) as date
                )
                When 'month12' THEN cast(
                    date_add(Strategy_Date, INTERVAL 11 MONTH) as date
                )
                When 'month13' THEN cast(
                    date_add(Strategy_Date, INTERVAL 12 MONTH) as date
                )
                When 'month14' THEN cast(
                    date_add(Strategy_Date, INTERVAL 13 MONTH) as date
                )
                When 'month15' THEN cast(
                    date_add(Strategy_Date, INTERVAL 14 MONTH) as date
                )
                When 'month16' THEN cast(
                    date_add(Strategy_Date, INTERVAL 15 MONTH) as date
                )
                When 'month17' THEN cast(
                    date_add(Strategy_Date, INTERVAL 16 MONTH) as date
                )
                When 'month18' THEN cast(
                    date_add(Strategy_Date, INTERVAL 17 MONTH) as date
                )
                When 'month19' THEN cast(
                    date_add(Strategy_Date, INTERVAL 18 MONTH) as date
                )
                When 'month20' THEN cast(
                    date_add(Strategy_Date, INTERVAL 19 MONTH) as date
                )
                When 'month21' THEN cast(
                    date_add(Strategy_Date, INTERVAL 20 MONTH) as date
                )
                When 'month22' THEN cast(
                    date_add(Strategy_Date, INTERVAL 21 MONTH) as date
                )
                When 'month23' THEN cast(
                    date_add(Strategy_Date, INTERVAL 22 MONTH) as date
                )
                When 'month24' THEN cast(
                    date_add(Strategy_Date, INTERVAL 23 MONTH) as date
                )
            end as Department_Date
        from (
                select c.name as `Client_Name`,
                    d.name as `Department_Name`,
                    s.name as `Strategy_Name`,
                    s.status as `Strategy_Status`,
                    s.type as `Strategy_Type`,
                    s.date as `Strategy_Date`,
                    s.created_at as `Strategy_Created_at`,
                    s.updated_at as ` Strategy_Updated_at`,
                    s.deleted_at as ` Strategy_Deleted_at`,
                    s.pillar_id,
                    p.name as `Pillar_Name`,
                    1 as Records,
                    s.monthly_gross_profit,
                    s.total_gross_profit,
                    s.id,
                    s.tenant_id,
                    s.client_id,
                    s.audit_id,
                    s.total_hours,
                    s.hourly_rate,
                    dr.length,
                    dr.department,
                    dr.month1,
                    dr.month2,
                    dr.month3,
                    dr.month4,
                    dr.month5,
                    dr.month6,
                    dr.month7,
                    dr.month8,
                    dr.month9,
                    dr.month10,
                    dr.month11,
                    dr.month12,
                    dr.month13,
                    dr.month14,
                    dr.month15,
                    dr.month16,
                    dr.month17,
                    dr.month18,
                    dr.month19,
                    dr.month20,
                    dr.month21,
                    dr.month22,
                    dr.month23,
                    dr.month24,
                    ts.service as `Service_Name`,
                    ts.task as `Task_name`,
                    ts.hours as `Task_Hours`
                from strategies as s
                    left join clients as c on s.client_id = c.id
                    left join strategy_department as sd on s.id = sd.strategy_id
                    left join departments as d on sd.department_id = d.id
                    left join pillars as p on s.pillar_id = p.id
                    left join (
                        SELECT s.name as service,
                            t.name as task,
                            st.hours,
                            st.strategy_id,
                            s.department_id
                        FROM strategy_task as st
                            LEFT JOIN tasks as t ON t.id = task_id
                            LEFT JOIN services as s ON s.id = service_id
                    ) as ts on ts.department_id = d.id
                    and ts.strategy_id = s.id
                    left join (
                        SELECT d1.id as blueprint,
                            d1.start,
                            d1.length,
                            d1.department,
                            round(
                                (
                                    (sm1.retainer * 0.7) - IFNULL(sum(sc.month_1), 0)
                                ) / sm1.hours * month1 + IFNULL(sum(sc.month_1), 0)
                            ) as month1,
                            round(
                                (
                                    (sm2.retainer * 0.7) - IFNULL(sum(sc.month_2), 0)
                                ) / sm2.hours * month2 + IFNULL(sum(sc.month_2), 0)
                            ) as month2,
                            round(
                                (
                                    (sm3.retainer * 0.7) - IFNULL(sum(sc.month_3), 0)
                                ) / sm3.hours * month3 + IFNULL(sum(sc.month_3), 0)
                            ) as month3,
                            round(
                                (
                                    (sm4.retainer * 0.7) - IFNULL(sum(sc.month_4), 0)
                                ) / sm4.hours * month4 + IFNULL(sum(sc.month_4), 0)
                            ) as month4,
                            round(
                                (
                                    (sm5.retainer * 0.7) - IFNULL(sum(sc.month_5), 0)
                                ) / sm5.hours * month5 + IFNULL(sum(sc.month_5), 0)
                            ) as month5,
                            round(
                                (
                                    (sm6.retainer * 0.7) - IFNULL(sum(sc.month_6), 0)
                                ) / sm6.hours * month6 + IFNULL(sum(sc.month_6), 0)
                            ) as month6,
                            round(
                                (
                                    (sm7.retainer * 0.7) - IFNULL(sum(sc.month_7), 0)
                                ) / sm7.hours * month7 + IFNULL(sum(sc.month_7), 0)
                            ) as month7,
                            round(
                                (
                                    (sm8.retainer * 0.7) - IFNULL(sum(sc.month_8), 0)
                                ) / sm8.hours * month8 + IFNULL(sum(sc.month_8), 0)
                            ) as month8,
                            round(
                                (
                                    (sm9.retainer * 0.7) - IFNULL(sum(sc.month_9), 0)
                                ) / sm9.hours * month9 + IFNULL(sum(sc.month_9), 0)
                            ) as month9,
                            round(
                                (
                                    (sm10.retainer * 0.7) - IFNULL(sum(sc.month_10), 0)
                                ) / sm10.hours * month10 + IFNULL(sum(sc.month_10), 0)
                            ) as month10,
                            round(
                                (
                                    (sm11.retainer * 0.7) - IFNULL(sum(sc.month_11), 0)
                                ) / sm11.hours * month11 + IFNULL(sum(sc.month_11), 0)
                            ) as month11,
                            round(
                                (
                                    (sm12.retainer * 0.7) - IFNULL(sum(sc.month_12), 0)
                                ) / sm12.hours * month12 + IFNULL(sum(sc.month_12), 0)
                            ) as month12,
                            round(
                                (
                                    (sm13.retainer * 0.7) - IFNULL(sum(sc.month_13), 0)
                                ) / sm13.hours * month13 + IFNULL(sum(sc.month_13), 0)
                            ) as month13,
                            round(
                                (
                                    (sm14.retainer * 0.7) - IFNULL(sum(sc.month_14), 0)
                                ) / sm14.hours * month14 + IFNULL(sum(sc.month_14), 0)
                            ) as month14,
                            round(
                                (
                                    (sm15.retainer * 0.7) - IFNULL(sum(sc.month_15), 0)
                                ) / sm15.hours * month15 + IFNULL(sum(sc.month_15), 0)
                            ) as month15,
                            round(
                                (
                                    (sm16.retainer * 0.7) - IFNULL(sum(sc.month_16), 0)
                                ) / sm16.hours * month16 + IFNULL(sum(sc.month_16), 0)
                            ) as month16,
                            round(
                                (
                                    (sm17.retainer * 0.7) - IFNULL(sum(sc.month_17), 0)
                                ) / sm17.hours * month17 + IFNULL(sum(sc.month_17), 0)
                            ) as month17,
                            round(
                                (
                                    (sm18.retainer * 0.7) - IFNULL(sum(sc.month_18), 0)
                                ) / sm18.hours * month18 + IFNULL(sum(sc.month_18), 0)
                            ) as month18,
                            round(
                                (
                                    (sm19.retainer * 0.7) - IFNULL(sum(sc.month_19), 0)
                                ) / sm19.hours * month19 + IFNULL(sum(sc.month_19), 0)
                            ) as month19,
                            round(
                                (
                                    (sm20.retainer * 0.7) - IFNULL(sum(sc.month_20), 0)
                                ) / sm20.hours * month20 + IFNULL(sum(sc.month_20), 0)
                            ) as month20,
                            round(
                                (
                                    (sm21.retainer * 0.7) - IFNULL(sum(sc.month_21), 0)
                                ) / sm21.hours * month21 + IFNULL(sum(sc.month_21), 0)
                            ) as month21,
                            round(
                                (
                                    (sm22.retainer * 0.7) - IFNULL(sum(sc.month_22), 0)
                                ) / sm22.hours * month22 + IFNULL(sum(sc.month_22), 0)
                            ) as month22,
                            round(
                                (
                                    (sm23.retainer * 0.7) - IFNULL(sum(sc.month_23), 0)
                                ) / sm23.hours * month23 + IFNULL(sum(sc.month_23), 0)
                            ) as month23,
                            round(
                                (
                                    (sm24.retainer * 0.7) - IFNULL(sum(sc.month_24), 0)
                                ) / sm24.hours * month24 + IFNULL(sum(sc.month_24), 0)
                            ) as month24
                        FROM (
                                SELECT s.id,
                                    s.length,
                                    s.total_retainer,
                                    s.date as start,
                                    d.id as department_id,
                                    d.name as department,
                                    CASE
                                        WHEN s.length >= 1 THEN sum(st.month_1)
                                        ELSE 0
                                    END as month1,
                                    CASE
                                        WHEN s.length >= 2 THEN sum(st.month_2)
                                        ELSE 0
                                    END as month2,
                                    CASE
                                        WHEN s.length >= 3 THEN sum(st.month_3)
                                        ELSE 0
                                    END as month3,
                                    CASE
                                        WHEN s.length >= 4 THEN sum(st.month_4)
                                        ELSE 0
                                    END as month4,
                                    CASE
                                        WHEN s.length >= 5 THEN sum(st.month_5)
                                        ELSE 0
                                    END as month5,
                                    CASE
                                        WHEN s.length >= 6 THEN sum(st.month_6)
                                        ELSE 0
                                    END as month6,
                                    CASE
                                        WHEN s.length >= 7 THEN sum(st.month_7)
                                        ELSE 0
                                    END as month7,
                                    CASE
                                        WHEN s.length >= 8 THEN sum(st.month_8)
                                        ELSE 0
                                    END as month8,
                                    CASE
                                        WHEN s.length >= 9 THEN sum(st.month_9)
                                        ELSE 0
                                    END as month9,
                                    CASE
                                        WHEN s.length >= 10 THEN sum(st.month_10)
                                        ELSE 0
                                    END as month10,
                                    CASE
                                        WHEN s.length >= 11 THEN sum(st.month_11)
                                        ELSE 0
                                    END as month11,
                                    CASE
                                        WHEN s.length >= 12 THEN sum(st.month_12)
                                        ELSE 0
                                    END as month12,
                                    CASE
                                        WHEN s.length >= 13 THEN sum(st.month_13)
                                        ELSE 0
                                    END as month13,
                                    CASE
                                        WHEN s.length >= 14 THEN sum(st.month_14)
                                        ELSE 0
                                    END as month14,
                                    CASE
                                        WHEN s.length >= 15 THEN sum(st.month_15)
                                        ELSE 0
                                    END as month15,
                                    CASE
                                        WHEN s.length >= 16 THEN sum(st.month_16)
                                        ELSE 0
                                    END as month16,
                                    CASE
                                        WHEN s.length >= 17 THEN sum(st.month_17)
                                        ELSE 0
                                    END as month17,
                                    CASE
                                        WHEN s.length >= 18 THEN sum(st.month_18)
                                        ELSE 0
                                    END as month18,
                                    CASE
                                        WHEN s.length >= 19 THEN sum(st.month_19)
                                        ELSE 0
                                    END as month19,
                                    CASE
                                        WHEN s.length >= 20 THEN sum(st.month_20)
                                        ELSE 0
                                    END as month20,
                                    CASE
                                        WHEN s.length >= 21 THEN sum(st.month_21)
                                        ELSE 0
                                    END as month21,
                                    CASE
                                        WHEN s.length >= 22 THEN sum(st.month_22)
                                        ELSE 0
                                    END as month22,
                                    CASE
                                        WHEN s.length >= 23 THEN sum(st.month_23)
                                        ELSE 0
                                    END as month23,
                                    CASE
                                        WHEN s.length >= 24 THEN sum(st.month_24)
                                        ELSE 0
                                    END as month24
                                FROM strategies as s
                                    LEFT JOIN strategy_task as st ON s.id = st.strategy_id
                                    LEFT JOIN tasks as t ON task_id = t.id
                                    LEFT JOIN services as se ON se.id = service_id
                                    LEFT JOIN departments as d ON d.id = department_id
                                WHERE st.hours > 0
                                    /*
                                     
                                     and s.status = 'won'
                                     and s.type = 'retainer' 
                                     
                                     */
                                GROUP BY s.id,
                                    d.id
                            ) as d1
                            LEFT JOIN strategy_months as sm1 ON sm1.strategy_id = d1.id
                            and sm1.name = 1
                            AND sm1.deleted_at IS NULL
                            LEFT JOIN strategy_months as sm2 ON sm2.strategy_id = d1.id
                            and sm2.name = 2
                            AND sm2.deleted_at IS NULL
                            LEFT JOIN strategy_months as sm3 ON sm3.strategy_id = d1.id
                            and sm3.name = 3
                            AND sm3.deleted_at IS NULL
                            LEFT JOIN strategy_months as sm4 ON sm4.strategy_id = d1.id
                            and sm4.name = 4
                            AND sm4.deleted_at IS NULL
                            LEFT JOIN strategy_months as sm5 ON sm5.strategy_id = d1.id
                            and sm5.name = 5
                            AND sm5.deleted_at IS NULL
                            LEFT JOIN strategy_months as sm6 ON sm6.strategy_id = d1.id
                            and sm6.name = 6
                            AND sm6.deleted_at IS NULL
                            LEFT JOIN strategy_months as sm7 ON sm7.strategy_id = d1.id
                            and sm7.name = 7
                            AND sm7.deleted_at IS NULL
                            LEFT JOIN strategy_months as sm8 ON sm8.strategy_id = d1.id
                            and sm8.name = 8
                            AND sm8.deleted_at IS NULL
                            LEFT JOIN strategy_months as sm9 ON sm9.strategy_id = d1.id
                            and sm9.name = 9
                            AND sm9.deleted_at IS NULL
                            LEFT JOIN strategy_months as sm10 ON sm10.strategy_id = d1.id
                            and sm10.name = 10
                            AND sm10.deleted_at IS NULL
                            LEFT JOIN strategy_months as sm11 ON sm11.strategy_id = d1.id
                            and sm11.name = 11
                            AND sm11.deleted_at IS NULL
                            LEFT JOIN strategy_months as sm12 ON sm12.strategy_id = d1.id
                            and sm12.name = 12
                            AND sm12.deleted_at IS NULL
                            LEFT JOIN strategy_months as sm13 ON sm13.strategy_id = d1.id
                            and sm13.name = 13
                            AND sm13.deleted_at IS NULL
                            LEFT JOIN strategy_months as sm14 ON sm14.strategy_id = d1.id
                            and sm14.name = 14
                            AND sm14.deleted_at IS NULL
                            LEFT JOIN strategy_months as sm15 ON sm15.strategy_id = d1.id
                            and sm15.name = 15
                            AND sm15.deleted_at IS NULL
                            LEFT JOIN strategy_months as sm16 ON sm16.strategy_id = d1.id
                            and sm16.name = 16
                            AND sm16.deleted_at IS NULL
                            LEFT JOIN strategy_months as sm17 ON sm17.strategy_id = d1.id
                            and sm17.name = 17
                            AND sm17.deleted_at IS NULL
                            LEFT JOIN strategy_months as sm18 ON sm18.strategy_id = d1.id
                            and sm18.name = 18
                            AND sm18.deleted_at IS NULL
                            LEFT JOIN strategy_months as sm19 ON sm19.strategy_id = d1.id
                            and sm19.name = 19
                            AND sm19.deleted_at IS NULL
                            LEFT JOIN strategy_months as sm20 ON sm20.strategy_id = d1.id
                            and sm20.name = 20
                            AND sm20.deleted_at IS NULL
                            LEFT JOIN strategy_months as sm21 ON sm21.strategy_id = d1.id
                            and sm21.name = 21
                            AND sm21.deleted_at IS NULL
                            LEFT JOIN strategy_months as sm22 ON sm22.strategy_id = d1.id
                            and sm22.name = 22
                            AND sm22.deleted_at IS NULL
                            LEFT JOIN strategy_months as sm23 ON sm23.strategy_id = d1.id
                            and sm23.name = 23
                            AND sm23.deleted_at IS NULL
                            LEFT JOIN strategy_months as sm24 ON sm24.strategy_id = d1.id
                            and sm24.name = 24
                            AND sm24.deleted_at IS NULL
                            LEFT JOIN strategy_costs as sc ON sc.strategy_id = d1.id
                            AND sc.department_id = d1.department_id
                        GROUP BY d1.id,
                            d1.department_id
                        ORDER BY d1.id,
                            d1.department
                    ) as dr on blueprint = s.id
                    and d.name = dr.department
            ) as base_table
            cross join (
                select 'month1' as Month
                UNION ALL
                select 'month2' as Month
                UNION ALL
                select 'month3' as Month
                UNION ALL
                select 'month4' as Month
                UNION ALL
                select 'month5' as Month
                UNION ALL
                select 'month6' as Month
                UNION ALL
                select 'month7' as Month
                UNION ALL
                select 'month8' as Month
                UNION ALL
                select 'month9' as Month
                UNION ALL
                select 'month10' as Month
                UNION ALL
                select 'month11' as Month
                UNION ALL
                select 'month12' as Month
                UNION ALL
                select 'month13' as Month
                UNION ALL
                select 'month14' as Month
                UNION ALL
                select 'month15' as Month
                UNION ALL
                select 'month16' as Month
                UNION ALL
                select 'month17' as Month
                UNION ALL
                select 'month18' as Month
                UNION ALL
                select 'month19' as Month
                UNION ALL
                select 'month20' as Month
                UNION ALL
                select 'month21' as Month
                UNION ALL
                select 'month22' as Month
                UNION ALL
                select 'month23' as Month
                UNION ALL
                select 'month24' as Month
            ) as dates
    ) as final_table
where id = 7333