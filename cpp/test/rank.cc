#include <phevaluator/phevaluator.h>

#include <algorithm>
#include <cassert>
#include <cstdio>

#include "gtest/gtest.h"
#include "kev/kev_eval.h"

using namespace phevaluator;

TEST(RankTest, TestValue) {
  Rank a = EvaluateCards("9c", "4c", "4s", "9d", "4h");
  Rank b = EvaluateCards("9c", "4c", "4s", "9d", "9h");

  ASSERT_EQ(a.value(), 292);
  ASSERT_EQ(b.value(), 236);
}

TEST(RankTest, TestComparison) {
  Rank a = EvaluateCards("9c", "4c", "4s", "9d", "4h");
  Rank b = EvaluateCards("9c", "4c", "4s", "9d", "9h");

  ASSERT_GT(b, a);
  ASSERT_GE(b, a);
  ASSERT_LT(a, b);
  ASSERT_LE(a, b);
  ASSERT_NE(a, b);
  ASSERT_TRUE(a != b);
}

TEST(RankTest, TestRankCategory) {
  Rank a = EvaluateCards("9c", "4c", "4s", "9d", "4h");
  Rank b = EvaluateCards("As", "Ks", "Qs", "Js", "Ts");

  ASSERT_EQ(a.category(), rank_category::FULL_HOUSE);
  ASSERT_EQ(b.category(), rank_category::STRAIGHT_FLUSH);

  ASSERT_EQ(a.describeCategory(), "Full House");
  ASSERT_EQ(b.describeCategory(), "Straight Flush");
}

TEST(RankTest, TestRankCategoryStraightFlushes) {
  Rank a = EvaluateCards("Ac", "Kc", "Qc", "Jc", "Tc");
  Rank b = EvaluateCards("2d", "3d", "4d", "5d", "6d");
  Rank c = EvaluateCards("Th", "7h", "9h", "6h", "8h");

  ASSERT_EQ(a.category(), rank_category::STRAIGHT_FLUSH);
  ASSERT_EQ(b.category(), rank_category::STRAIGHT_FLUSH);
  ASSERT_EQ(c.category(), rank_category::STRAIGHT_FLUSH);

  ASSERT_EQ(a.describeCategory(), "Straight Flush");
  ASSERT_EQ(b.describeCategory(), "Straight Flush");
  ASSERT_EQ(c.describeCategory(), "Straight Flush");
}

TEST(RankTest, TestRankCategoryFourOfAKinds) {
  Rank a = EvaluateCards("Ac", "Ad", "As", "Ah", "Ks");
  Rank b = EvaluateCards("2d", "2s", "2c", "2h", "3s");
  Rank c = EvaluateCards("Th", "Ts", "Tc", "Td", "7d");

  ASSERT_EQ(a.category(), rank_category::FOUR_OF_A_KIND);
  ASSERT_EQ(b.category(), rank_category::FOUR_OF_A_KIND);
  ASSERT_EQ(c.category(), rank_category::FOUR_OF_A_KIND);

  ASSERT_EQ(a.describeCategory(), "Four of a Kind");
  ASSERT_EQ(b.describeCategory(), "Four of a Kind");
  ASSERT_EQ(c.describeCategory(), "Four of a Kind");
}

TEST(RankTest, TestRankCategoryFullHouses) {
  Rank a = EvaluateCards("Ac", "Ad", "Kc", "Kh", "Ks");
  Rank b = EvaluateCards("2d", "3d", "2c", "3h", "3s");
  Rank c = EvaluateCards("7h", "8s", "8h", "8c", "7d");

  ASSERT_EQ(a.category(), rank_category::FULL_HOUSE);
  ASSERT_EQ(b.category(), rank_category::FULL_HOUSE);
  ASSERT_EQ(c.category(), rank_category::FULL_HOUSE);

  ASSERT_EQ(a.describeCategory(), "Full House");
  ASSERT_EQ(b.describeCategory(), "Full House");
  ASSERT_EQ(c.describeCategory(), "Full House");
}

TEST(RankTest, TestRankCategoryFlushes) {
  Rank a = EvaluateCards("Ac", "2c", "7c", "Jc", "Tc");
  Rank b = EvaluateCards("Kd", "3d", "8d", "Td", "5d");
  Rank c = EvaluateCards("Jh", "5h", "4h", "9h", "Th");

  ASSERT_EQ(a.category(), rank_category::FLUSH);
  ASSERT_EQ(b.category(), rank_category::FLUSH);
  ASSERT_EQ(c.category(), rank_category::FLUSH);

  ASSERT_EQ(a.describeCategory(), "Flush");
  ASSERT_EQ(b.describeCategory(), "Flush");
  ASSERT_EQ(c.describeCategory(), "Flush");
}

TEST(RankTest, TestRankCategoryStraights) {
  Rank a = EvaluateCards("Ac", "Kd", "Qs", "Jh", "Tc");
  Rank b = EvaluateCards("Kd", "Qs", "Js", "Th", "9d");
  Rank c = EvaluateCards("6h", "5s", "4s", "3d", "2c");

  ASSERT_EQ(a.category(), rank_category::STRAIGHT);
  ASSERT_EQ(b.category(), rank_category::STRAIGHT);
  ASSERT_EQ(c.category(), rank_category::STRAIGHT);

  ASSERT_EQ(a.describeCategory(), "Straight");
  ASSERT_EQ(b.describeCategory(), "Straight");
  ASSERT_EQ(c.describeCategory(), "Straight");
}

TEST(RankTest, TestRankCategoryThreeOfAKinds) {
  Rank a = EvaluateCards("Ac", "Ad", "As", "Jh", "Tc");
  Rank b = EvaluateCards("3d", "2s", "Js", "3h", "3c");
  Rank c = EvaluateCards("8h", "5s", "5d", "3d", "5c");

  ASSERT_EQ(a.category(), rank_category::THREE_OF_A_KIND);
  ASSERT_EQ(b.category(), rank_category::THREE_OF_A_KIND);
  ASSERT_EQ(c.category(), rank_category::THREE_OF_A_KIND);

  ASSERT_EQ(a.describeCategory(), "Three of a Kind");
  ASSERT_EQ(b.describeCategory(), "Three of a Kind");
  ASSERT_EQ(c.describeCategory(), "Three of a Kind");
}

TEST(RankTest, TestRankCategoryTwoPairs) {
  Rank a = EvaluateCards("Ac", "Ad", "Js", "Jh", "Tc");
  Rank b = EvaluateCards("3d", "2s", "Js", "2h", "3c");
  Rank c = EvaluateCards("8h", "7s", "5d", "8d", "5c");

  ASSERT_EQ(a.category(), rank_category::TWO_PAIR);
  ASSERT_EQ(b.category(), rank_category::TWO_PAIR);
  ASSERT_EQ(c.category(), rank_category::TWO_PAIR);

  ASSERT_EQ(a.describeCategory(), "Two Pair");
  ASSERT_EQ(b.describeCategory(), "Two Pair");
  ASSERT_EQ(c.describeCategory(), "Two Pair");
}

TEST(RankTest, TestRankCategoryOnePairs) {
  Rank a = EvaluateCards("Ac", "Ad", "7s", "Jh", "Tc");
  Rank b = EvaluateCards("9d", "2s", "Js", "2h", "3c");
  Rank c = EvaluateCards("2h", "6s", "5d", "8d", "5c");

  ASSERT_EQ(a.category(), rank_category::ONE_PAIR);
  ASSERT_EQ(b.category(), rank_category::ONE_PAIR);
  ASSERT_EQ(c.category(), rank_category::ONE_PAIR);

  ASSERT_EQ(a.describeCategory(), "One Pair");
  ASSERT_EQ(b.describeCategory(), "One Pair");
  ASSERT_EQ(c.describeCategory(), "One Pair");
}

TEST(RankTest, TestRankCategoryHighCards) {
  Rank a = EvaluateCards("Ac", "2d", "7s", "Jh", "Tc");
  Rank b = EvaluateCards("9d", "2s", "6c", "Ts", "3c");
  Rank c = EvaluateCards("2h", "Qs", "5d", "7d", "3c");

  ASSERT_EQ(a.category(), rank_category::HIGH_CARD);
  ASSERT_EQ(b.category(), rank_category::HIGH_CARD);
  ASSERT_EQ(c.category(), rank_category::HIGH_CARD);

  ASSERT_EQ(a.describeCategory(), "High Card");
  ASSERT_EQ(b.describeCategory(), "High Card");
  ASSERT_EQ(c.describeCategory(), "High Card");
}

TEST(RankTest, TestRankDescription) {
  Rank a = EvaluateCards("9c", "4c", "4s", "9d", "4h");
  Rank b = EvaluateCards("As", "Ks", "Qs", "Js", "Ts");

  ASSERT_EQ(a.describeRank(), "Fours Full over Nines");
  ASSERT_EQ(b.describeRank(), "Royal Flush");

  ASSERT_EQ(a.describeSampleHand(), "44499");
  ASSERT_EQ(b.describeSampleHand(), "AKQJT");

  ASSERT_FALSE(a.isFlush());
  ASSERT_TRUE(b.isFlush());
}

TEST(RankTest, TestRankDescriptionStraightFlushes) {
  Rank a = EvaluateCards("6s", "2s", "5s", "3s", "4s");
  Rank b = EvaluateCards("8d", "Td", "Jd", "Qd", "9d");
  Rank c = EvaluateCards("6h", "8h", "5h", "7h", "4h");

  ASSERT_EQ(a.describeRank(), "Six-High Straight Flush");
  ASSERT_EQ(b.describeRank(), "Queen-High Straight Flush");
  ASSERT_EQ(c.describeRank(), "Eight-High Straight Flush");

  ASSERT_EQ(a.describeSampleHand(), "65432");
  ASSERT_EQ(b.describeSampleHand(), "QJT98");
  ASSERT_EQ(c.describeSampleHand(), "87654");

  ASSERT_TRUE(a.isFlush());
  ASSERT_TRUE(b.isFlush());
  ASSERT_TRUE(c.isFlush());
}

TEST(RankTest, TestRankDescriptionFourOfAKinds) {
  Rank a = EvaluateCards("As", "Ad", "Ac", "2s", "Ah");
  Rank b = EvaluateCards("Qs", "Qc", "3d", "Qd", "Qh");
  Rank c = EvaluateCards("3d", "3c", "8c", "3h", "3s");

  ASSERT_EQ(a.describeRank(), "Four Aces");
  ASSERT_EQ(b.describeRank(), "Four Queens");
  ASSERT_EQ(c.describeRank(), "Four Treys");

  ASSERT_EQ(a.describeSampleHand(), "AAAA2");
  ASSERT_EQ(b.describeSampleHand(), "QQQQ3");
  ASSERT_EQ(c.describeSampleHand(), "33338");

  ASSERT_FALSE(a.isFlush());
  ASSERT_FALSE(b.isFlush());
  ASSERT_FALSE(c.isFlush());
}

TEST(RankTest, TestRankDescriptionFullHouses) {
  Rank a = EvaluateCards("As", "2d", "Ac", "2s", "Ah");
  Rank b = EvaluateCards("3c", "Qc", "3d", "3s", "Qh");
  Rank c = EvaluateCards("8d", "7d", "8c", "8s", "7h");

  ASSERT_EQ(a.describeRank(), "Aces Full over Deuces");
  ASSERT_EQ(b.describeRank(), "Treys Full over Queens");
  ASSERT_EQ(c.describeRank(), "Eights Full over Sevens");

  ASSERT_EQ(a.describeSampleHand(), "AAA22");
  ASSERT_EQ(b.describeSampleHand(), "333QQ");
  ASSERT_EQ(c.describeSampleHand(), "88877");

  ASSERT_FALSE(a.isFlush());
  ASSERT_FALSE(b.isFlush());
  ASSERT_FALSE(c.isFlush());
}

TEST(RankTest, TestRankDescriptionFlushes) {
  Rank a = EvaluateCards("As", "2s", "3s", "7s", "Ts");
  Rank b = EvaluateCards("2c", "Qc", "Tc", "7c", "4c");
  Rank c = EvaluateCards("2d", "4d", "3d", "8d", "5d");

  ASSERT_EQ(a.describeRank(), "Ace-High Flush");
  ASSERT_EQ(b.describeRank(), "Queen-High Flush");
  ASSERT_EQ(c.describeRank(), "Eight-High Flush");

  ASSERT_EQ(a.describeSampleHand(), "AT732");
  ASSERT_EQ(b.describeSampleHand(), "QT742");
  ASSERT_EQ(c.describeSampleHand(), "85432");

  ASSERT_TRUE(a.isFlush());
  ASSERT_TRUE(b.isFlush());
  ASSERT_TRUE(c.isFlush());
}

TEST(RankTest, TestRankDescriptionStraights) {
  Rank a = EvaluateCards("As", "Kc", "Qd", "Jd", "Th");
  Rank b = EvaluateCards("Ks", "Qc", "Jd", "Td", "9h");
  Rank c = EvaluateCards("5h", "4d", "3d", "2c", "As");

  ASSERT_EQ(a.describeRank(), "Ace-High Straight");
  ASSERT_EQ(b.describeRank(), "King-High Straight");
  ASSERT_EQ(c.describeRank(), "Five-High Straight");

  ASSERT_EQ(a.describeSampleHand(), "AKQJT");
  ASSERT_EQ(b.describeSampleHand(), "KQJT9");
  ASSERT_EQ(c.describeSampleHand(), "5432A");

  ASSERT_FALSE(a.isFlush());
  ASSERT_FALSE(b.isFlush());
  ASSERT_FALSE(c.isFlush());

  ASSERT_EQ(a.category(), rank_category::STRAIGHT);
  ASSERT_EQ(b.category(), rank_category::STRAIGHT);
  ASSERT_EQ(c.category(), rank_category::STRAIGHT);
}

TEST(RankTest, TestRankDescriptionThreeOfAKinds) {
  Rank a = EvaluateCards("As", "2s", "Ad", "Ac", "Ts");
  Rank b = EvaluateCards("6d", "6c", "2h", "6s", "4c");
  Rank c = EvaluateCards("9s", "4d", "9d", "8d", "9h");

  ASSERT_EQ(a.describeRank(), "Three Aces");
  ASSERT_EQ(b.describeRank(), "Three Sixes");
  ASSERT_EQ(c.describeRank(), "Three Nines");

  ASSERT_EQ(a.describeSampleHand(), "AAAT2");
  ASSERT_EQ(b.describeSampleHand(), "66642");
  ASSERT_EQ(c.describeSampleHand(), "99984");

  ASSERT_FALSE(a.isFlush());
  ASSERT_FALSE(b.isFlush());
  ASSERT_FALSE(c.isFlush());
}

TEST(RankTest, TestRankDescriptionTwoPairs) {
  Rank a = EvaluateCards("As", "2s", "Ad", "Tc", "Ts");
  Rank b = EvaluateCards("6d", "2c", "4h", "6s", "4c");
  Rank c = EvaluateCards("9s", "7d", "9d", "7s", "Ah");

  ASSERT_EQ(a.describeRank(), "Aces and Tens");
  ASSERT_EQ(b.describeRank(), "Sixes and Fours");
  ASSERT_EQ(c.describeRank(), "Nines and Sevens");

  ASSERT_EQ(a.describeSampleHand(), "AATT2");
  ASSERT_EQ(b.describeSampleHand(), "66442");
  ASSERT_EQ(c.describeSampleHand(), "9977A");

  ASSERT_FALSE(a.isFlush());
  ASSERT_FALSE(b.isFlush());
  ASSERT_FALSE(c.isFlush());
}

TEST(RankTest, TestRankDescriptionOnePairs) {
  Rank a = EvaluateCards("Qs", "2s", "Qh", "3c", "Ts");
  Rank b = EvaluateCards("5s", "2c", "3h", "6s", "3c");
  Rank c = EvaluateCards("Ts", "Qd", "Td", "7s", "Ah");

  ASSERT_EQ(a.describeRank(), "Pair of Queens");
  ASSERT_EQ(b.describeRank(), "Pair of Treys");
  ASSERT_EQ(c.describeRank(), "Pair of Tens");

  ASSERT_EQ(a.describeSampleHand(), "QQT32");
  ASSERT_EQ(b.describeSampleHand(), "33652");
  ASSERT_EQ(c.describeSampleHand(), "TTAQ7");

  ASSERT_FALSE(a.isFlush());
  ASSERT_FALSE(b.isFlush());
  ASSERT_FALSE(c.isFlush());
}

TEST(RankTest, TestRankDescriptionHighCards) {
  Rank a = EvaluateCards("6s", "7s", "2d", "3c", "4h");
  Rank b = EvaluateCards("Qs", "3c", "Ah", "Kc", "2d");
  Rank c = EvaluateCards("4h", "9s", "Td", "7s", "2d");

  ASSERT_EQ(a.describeRank(), "Seven-High");
  ASSERT_EQ(b.describeRank(), "Ace-High");
  ASSERT_EQ(c.describeRank(), "Ten-High");

  ASSERT_EQ(a.describeSampleHand(), "76432");
  ASSERT_EQ(b.describeSampleHand(), "AKQ32");
  ASSERT_EQ(c.describeSampleHand(), "T9742");

  ASSERT_FALSE(a.isFlush());
  ASSERT_FALSE(b.isFlush());
  ASSERT_FALSE(c.isFlush());
}
