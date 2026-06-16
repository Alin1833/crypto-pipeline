{{ config(materialized='table') }}

with sursa as (
    select * from {{ ref('stg_coins') }}
),

agregate as (
    select
        coin_id,
        date_trunc('day', fetched_at) as price_date,
        min(price_usd) as price_min,
        max(price_usd) as price_max,
        avg(price_usd) as price_avg,
        sum(volume_24h) as total_volume,
        count(*) as nr_colectari
    from sursa
    group by 1, 2
)

select * from agregate