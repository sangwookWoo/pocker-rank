
CREATE OR REPLACE FUNCTION get_head_to_head_record(player_names text[])
RETURNS TABLE (name text, wins integer) AS $$
BEGIN
    RETURN QUERY
    WITH target_players AS (
        -- player_names 배열에 해당하는 player_id들을 찾는 쿼리
        SELECT id
        FROM players as p
        WHERE p.name = ANY(player_names)
    ),
    target_games AS (
        -- target_players의 player_id들이 참여한 게임을 찾는 쿼리
        SELECT played_at
        FROM rankings
        WHERE player_id IN (SELECT id FROM target_players)
        GROUP BY played_at
        HAVING COUNT(DISTINCT player_id) = 2  -- 2명만 참여한 게임만 선택
    ),
    ranked_players AS (
        -- 참여한 게임에서 각 플레이어의 정보를 가져오는 쿼리
        SELECT *
        FROM rankings
        WHERE played_at IN (SELECT played_at FROM target_games)
          AND player_id IN (SELECT id FROM target_players)
    ),
    win_counts AS (
        -- 각 게임에서 승리한 플레이어 수를 세는 쿼리
        SELECT 
            p1.player_id AS player_id,
            COUNT(*) AS wins
        FROM ranked_players p1
        JOIN ranked_players p2 
            ON p1.played_at = p2.played_at 
            AND p1.player_id != p2.player_id
        WHERE p1.rank < p2.rank  -- p1이 더 높은 순위일 때 승리
        GROUP BY p1.player_id
    )
    -- 최종적으로 각 플레이어의 이름과 승리 횟수를 출력
    select p.name::text, COALESCE(w.wins, 0)::integer AS wins
    FROM win_counts AS w
    INNER JOIN players AS p
      ON w.player_id = p.id;
END;
$$ LANGUAGE plpgsql;
