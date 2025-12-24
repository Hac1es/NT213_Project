export function calculateEverything(mapping, userScores, weights) {
  const results = mapping.map((aspectObj) => {
    // Tầng 4: CRITERION
    const criteriaScores = aspectObj.criteria
      .map((crit) => {
        let passCount = 0; // Điểm 1 (Xanh)
        let partialCount = 0; // Điểm 0.5 (Vàng)
        let failCount = 0; // Điểm 0 (Đỏ)

        // Tầng 3: ELEMENT
        const elementScores = crit.elements
          .map((elem) => {
            // Tầng 2: MECHANISM
            const mechanismScores = elem.mechanisms
              .map((mech) => {
                const reqValues = mech.requirements.map((reqId) => {
                  const val = userScores[reqId];

                  // THỰC HIỆN ĐẾM TẠI ĐÂY
                  if (val === 1) passCount++;
                  else if (val === 0.5) partialCount++;
                  else if (val === 0) failCount++;

                  return val;
                });

                const activeScores = reqValues.filter(
                  (s) => typeof s === "number"
                );
                // Tầng 1: REQUIREMENT
                const score =
                  activeScores.length > 0
                    ? activeScores.reduce((a, b) => a + b, 0) /
                      activeScores.length
                    : null;

                return {
                  name: mech.mechanism,
                  score,
                  requirements: mech.requirements,
                };
              })
              .filter((m) => m.score !== null);

            const elemScore =
              mechanismScores.length > 0
                ? mechanismScores.reduce((a, b) => a + b.score, 0) /
                  mechanismScores.length
                : null;

            // Lưu lại mechanismDetails để Drill-down
            return {
              name: elem.element,
              score: elemScore,
              mechanismsDetails: mechanismScores,
            };
          })
          .filter((e) => e.score !== null);

        const critScore =
          elementScores.length > 0
            ? elementScores.reduce((a, b) => a + b.score, 0) /
              elementScores.length
            : null;

        // Lưu lại elementDetails
        return {
          name: crit.criterion,
          score: critScore,
          counts: {
            pass: passCount, // Số lượng cột Xanh
            partial: partialCount, // Số lượng cột Vàng
            fail: failCount, // Số lượng cột Đỏ
          },
          elementsDetails: elementScores,
        };
      })
      .filter((c) => c.score !== null);

    const aspectScore =
      criteriaScores.length > 0
        ? criteriaScores.reduce((a, b) => a + b.score, 0) /
          criteriaScores.length
        : 0;

    return {
      aspect: aspectObj.aspect,
      score: aspectScore,
      weight: weights[aspectObj.aspect] || 0,
      criteriaDetails: criteriaScores, // <--- "Vũ khí" để Drill-down đây!
    };
  });

  const totalWeightedScore = results.reduce(
    (sum, item) => sum + item.score * item.weight,
    0
  );
  const finalScore = totalWeightedScore * 10;

  return {
    soiScore: finalScore.toFixed(2),
    rating: getRating(finalScore),
    aspectDetails: results,
  };
}

function getRating(score) {
  if (score >= 9.0) return "Excellent Security";
  if (score >= 7.0) return "Good Security";
  if (score >= 4.0) return "Moderate Security";
  return "Weak Security";
}
