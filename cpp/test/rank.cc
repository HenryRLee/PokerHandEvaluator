#include <cstdio>
#include <cassert>
#include <algorithm>
#include <phevaluator/phevaluator.h>
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

  ASSERT_EQ(a.category(), FULL_HOUSE);
  ASSERT_EQ(b.category(), STRAIGHT_FLUSH);

  ASSERT_EQ(a.describeCategory(), "Full House");
  ASSERT_EQ(b.describeCategory(), "Straight Flush");
}

TEST(RankTest, TestRankDescription) {
  Rank a = EvaluateCards("9c", "4c", "4s", "9d", "4h");
	Rank b = EvaluateCards("As", "Ks", "Qs", "Js", "Ts");

  ASSERT_EQ(a.describeRank(), "Fours Full over Nines");
  ASSERT_EQ(b.describeRank(), "Royal Flush");

  ASSERT_EQ(a.describeSampleHand(), "4 4 4 9 9");
  ASSERT_EQ(b.describeSampleHand(), "A K Q J T");

  ASSERT_FALSE(a.isFlush());
  ASSERT_TRUE(b.isFlush());
}

TEST(RankTest, TestRankDescriptionStraights)
{
  Rank a = EvaluateCards("As", "Kc", "Qd", "Jd", "Th");
  Rank b = EvaluateCards("Ks", "Qc", "Jd", "Td", "9h");
  Rank c = EvaluateCards("5h", "4d", "3d", "2c", "As");

  ASSERT_EQ(a.describeRank(), "Ace-High Straight");
  ASSERT_EQ(b.describeRank(), "King-High Straight");
  ASSERT_EQ(c.describeRank(), "Five-High Straight");

  ASSERT_EQ(a.category(), STRAIGHT);
  ASSERT_EQ(b.category(), STRAIGHT);
  ASSERT_EQ(c.category(), STRAIGHT);
}
