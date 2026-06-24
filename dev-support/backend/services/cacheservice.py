# backend/cache/cache_service.py

CACHE = {}

CACHE_STATS = {

    "hits": 0,

    "misses": 0
}


def get_cached_response(query):

    query = query.lower().strip()

    if query in CACHE:

        CACHE_STATS["hits"] += 1

        print(
            f"\nCACHE HIT: {query}"
        )

        return CACHE[query]

    CACHE_STATS["misses"] += 1

    print(
        f"\nCACHE MISS: {query}"
    )

    return None


def set_cached_response(query, response):
    query = query.lower().strip()

    # don't cache short follow-up queries — they depend on context
    if len(query.split()) <= 5:
        print(f"CACHE SKIP (short query): {query}")
        return

    CACHE[query] = response

def get_cache_stats():

    total = (

        CACHE_STATS["hits"]

        +

        CACHE_STATS["misses"]
    )

    hit_ratio = 0

    if total > 0:

        hit_ratio = round(

            (
                CACHE_STATS["hits"]

                /

                total
            ) * 100,

            2
        )

    return {

        "cache_size":
            len(CACHE),

        "cache_hits":
            CACHE_STATS["hits"],

        "cache_misses":
            CACHE_STATS["misses"],

        "hit_ratio":
            hit_ratio
    }