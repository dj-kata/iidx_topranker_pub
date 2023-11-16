# iidx_topranker_pubとは
IIDXSP全1botの公開データ管理用レポジトリです。

# コンテンツ
- [iidx29.tsv](https://github.com/dj-kata/iidx_topranker_pub/blob/main/iidx29.tsv): IIDX29(CastHour)時点での曲情報(レベル、ノーツ数、歴代全1、全1)
- [sp.tsv](https://github.com/dj-kata/iidx_topranker_pub/blob/main/sp.tsv): 現行作での曲情報
- README.md: 本ファイル

# TSVについて
sp.tsvのコミット履歴から曲追加や全1更新の履歴を追えるようにしています。  
[Twilog](https://twilog.org/iidx_topranker)のサービス終了に伴う対応となります。

歴代全1スコアについては、toprankerページにアクセス可能なHEROIC VERSE以降で最も高いスコアを使っています(自動集計済み)。
また、難易度については一部手で入力した曲があります。
間違っているものがありましたら、教えていただけると助かります。

## フォーマット
botから直接使っているためタイトル行を追加していませんが、フォーマットは以下。
```
曲名___譜面, バージョンフォルダ, 難易度, ノーツ数, 歴代全1の{バージョン, エリア, DJ NAME, スコア}, 現行全1の{エリア, DJ NAME
, スコア}
```

## 運用方法
1日1回自動コミットします。  
pushは手動実行のためレポジトリに反映されるタイミングは不定です。
