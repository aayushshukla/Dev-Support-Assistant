def build_context(results):

    context_parts = []

    for idx, result in enumerate(
            results,
            start=1
    ):

        context_parts.append(

            f"""
DOCUMENT {idx}

Title:
{result['title']}

Source:
{result['source_url']}

Content:
{result['chunk_text']}
            """
        )

    return "\n\n====================\n\n".join(
        context_parts
    )