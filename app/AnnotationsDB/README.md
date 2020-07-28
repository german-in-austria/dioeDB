# Annotations Tool

## Anno-sent
### Materialized View

Muss manuell erstellt werden:

```
CREATE MATERIALIZED VIEW mat_adhocsentences
  AS (
  SELECT row_number() OVER (PARTITION BY true) as id, z.adhoc_sentence, z.tokenids, z.infid, z.transid, z.tokreih, z.seqsent, z.sentorig, z.sentorth, lag(z.fallbacktext) OVER (order by z.adhoc_sentence asc) as left_context, z.senttext, lead(z.fallbacktext) OVER (order by z.adhoc_sentence asc) as right_context, z.sentttlemma, z.sentttpos, z.sentsplemma, z.sentsppos, z.sentsptag, z.sentspdep, z.sentspenttype
  FROM(
  SELECT
    y.adhoc_sentence,
    ARRAY_AGG(y.id ORDER BY y."ID_Inf_id", y.transcript_id_id, y.token_reihung asc) as tokenids,
    "y"."ID_Inf_id" as infid,
    "y"."transcript_id_id" as transid,
    ARRAY_AGG(y.token_reihung ORDER BY y."ID_Inf_id", y.transcript_id_id, y.token_reihung asc) as tokreih,
    ARRAY_AGG(y.sequence_in_sentence ORDER BY y."ID_Inf_id", y.transcript_id_id, y.token_reihung asc) as seqsent,
    string_agg("text", ' ' ORDER BY y."ID_Inf_id", y.transcript_id_id, y.token_reihung NULLS FIRST) as sentorig,
    string_agg(CASE
                  WHEN y.token_type_id_id = 1 AND y.fragment_of_id IS NOT NULL THEN NULL
                  ELSE "text" END, ' ' ORDER BY y."ID_Inf_id", y.transcript_id_id, y.token_reihung NULLS FIRST) as senttext,
    string_agg(CASE
                  WHEN y.token_type_id_id = 1 AND y.fragment_of_id IS NOT NULL THEN NULL
                  ELSE
                    CASE WHEN "text" IS NOT NULL THEN "text" ELSE
                      CASE WHEN "ortho" IS NOT NULL THEN "ortho" ELSE
                        CASE WHEN "text_in_ortho" IS NOT NULL THEN "text_in_ortho" ELSE "phon"
                        END
                      END
                    END
                  END, ' ' ORDER BY y."ID_Inf_id", y.transcript_id_id, y.token_reihung NULLS FIRST) as fallbacktext,
    string_agg(CASE
                  WHEN y.token_type_id_id = 1 AND y.fragment_of_id IS NOT NULL THEN NULL
                  WHEN "ortho" IS NOT NULL THEN "ortho" ELSE "text" END, ' '
                  ORDER BY y."ID_Inf_id", y.transcript_id_id, y.token_reihung NULLS FIRST) as sentorth,
    string_agg(y.ttlemma, ' ' ORDER BY y."ID_Inf_id", y.transcript_id_id, y.token_reihung NULLS FIRST) as sentttlemma,
    string_agg(y.ttpos, ' ' ORDER BY y."ID_Inf_id", y.transcript_id_id, y.token_reihung NULLS FIRST) as sentttpos,
    string_agg(y.splemma, ' ' ORDER BY y."ID_Inf_id", y.transcript_id_id, y.token_reihung NULLS FIRST) as sentsplemma,
    string_agg(y.sppos, ' ' ORDER BY y."ID_Inf_id", y.transcript_id_id, y.token_reihung NULLS FIRST) as sentsppos,
    string_agg(y.sptag, ' ' ORDER BY y."ID_Inf_id", y.transcript_id_id, y.token_reihung NULLS FIRST) as sentsptag,
    string_agg(CASE WHEN y.spenttype = '' OR y.spenttype IS NULL THEN '#' ELSE y.spenttype END, ' ' ORDER BY y."ID_Inf_id", y.transcript_id_id, y.token_reihung NULLS FIRST) as sentspenttype,
    string_agg(y.spdep, ' ' ORDER BY y."ID_Inf_id", y.transcript_id_id, y.token_reihung NULLS FIRST) as sentspdep
      FROM
      (SELECT *,count(is_start OR NULL) OVER (order by x."ID_Inf_id", x.transcript_id_id, x.token_reihung asc) as adhoc_sentence
        FROM (
        SELECT *,
          CASE WHEN lag(t.token_type_id_id) Over (order by  t."ID_Inf_id", t.transcript_id_id, t.token_reihung asc) = 2 THEN TRUE ELSE FALSE end as is_start
          from "token" t
          order by t."ID_Inf_id", t.transcript_id_id, t.token_reihung
        ) x
        ORDER BY x."ID_Inf_id", x.transcript_id_id, x.token_reihung
      ) y
      Group By adhoc_sentence, "y"."ID_Inf_id", "y"."transcript_id_id"
    ) z
  );
create unique index on mat_adhocsentences (id);
```

Vorhandene Materialized View löschen

```
DROP MATERIALIZED VIEW mat_adhocsentences
```
