/*!
 * \file
 * \brief seed_seq の入力数による初期段階の乱数列への影響の調査
 */

// TODO ChatGPT の出力のままで、変数名が適当になっているのを修正する。

#include <bit>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <random>
#include <vector>

int main() {
    const int M = 100;        // 位置（最初の M 個を見る）
    const int trials = 300;   // 試行回数
    const std::vector<int> ks = {1, 2, 4, 8, 16};

    // 再現性のため固定シードの生成器（seed の材料を作る）
    std::mt19937_64 seed_gen(123456789);

    std::ofstream ofs("test_num_seeds.csv");
    if (!ofs) {
        std::cerr << "Failed to open output CSV.\n";
        return 1;
    }

    // CSV ヘッダ
    ofs << "num_seeds,pos,avg_popcount\n";

    for (int k : ks) {
        std::vector<std::uint64_t> sum_pop(M, 0);

        for (int t = 0; t < trials; ++t) {
            // 試行ごとに異なる base seed を生成（ただし seed_gen が固定なので再現性あり）
            std::vector<std::uint32_t> base(k);
            for (int i = 0; i < k; ++i) {
                base[i] = static_cast<std::uint32_t>(seed_gen());
            }

            auto a = base;
            auto b = base;

            // 近傍 seed：最後の 1 ワードの 1 ビットだけ反転
            const int bit = t % 32;
            b.back() ^= (1u << bit);

            std::seed_seq ssa(a.begin(), a.end());
            std::seed_seq ssb(b.begin(), b.end());

            using random_engine_type = std::mt19937;
            random_engine_type ra(ssa);
            random_engine_type rb(ssb);

            for (int pos = 0; pos < M; ++pos) {
                std::uint32_t xa = ra();
                std::uint32_t xb = rb();
                sum_pop[pos] += std::popcount(xa ^ xb);
            }
        }

        for (int pos = 0; pos < M; ++pos) {
            double avg = static_cast<double>(sum_pop[pos]) / static_cast<double>(trials);
            ofs << k << "," << pos << "," << avg << "\n";
        }
    }

    std::cerr << "Wrote test_num_seeds.csv\n";
    return 0;
}
