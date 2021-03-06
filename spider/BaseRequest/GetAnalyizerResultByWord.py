from BaseRequest.BaseApi import BaseApi


class GetAnalyizerResultByWord(BaseApi):

    @staticmethod
    async def get(session, form):
        params = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {
                                "keyword": form.word.data
                            }
                        },
                        {
                            "match": {
                                "category": form.category.data
                            }
                        }
                    ],
                    "must_not": {
                        "term": {
                            "is_delete": 'true'
                        }
                    }
                }
            },
            "sort": [
                {
                    "leftavgclick7days": {
                        "order": "desc"
                    }
                }
            ]
        }

        headers = {'Content-Type': 'application/json'}

        async with session.get('http://localhost:9200/keywords/_search',
                               timeout=5,
                               json=params,
                               headers=headers) as resp:
            text = await resp.text()

        return text
