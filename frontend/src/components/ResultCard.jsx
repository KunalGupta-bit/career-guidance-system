import {
  Award,
  AlertTriangle,
  CheckCircle2,
  TrendingUp,
} from "lucide-react";

export default function ResultCard({ result }) {
  if (!result) return null;

  const avgMatch =
    result.resume_score ??
    Math.round(
      result.top_recommendations.reduce(
        (sum, r) => sum + r.match_percentage,
        0
      ) / result.top_recommendations.length
    );

  const scoreColor =
    avgMatch >= 75
      ? "from-green-500 to-emerald-500"
      : avgMatch >= 55
      ? "from-yellow-400 to-orange-500"
      : "from-red-400 to-pink-500";

  return (
    <div className="mt-8 max-w-full sm:max-w-4xl mx-auto bg-white/80 backdrop-blur-xl p-6 sm:p-10 rounded-3xl shadow-2xl border border-gray-200">
      {/* HEADER */}
      <div className="flex flex-col sm:flex-row justify-between items-center gap-6 mb-8 sm:mb-10">
        <div className="text-center sm:text-left">
          <h2 className="text-2xl sm:text-3xl font-bold text-gray-800">
            AI Career Intelligence Report
          </h2>
          <p className="text-xs sm:text-sm text-gray-500 mt-1">
            Deep analysis of your resume & career alignment
          </p>
        </div>

        {/* SCORE RING */}
        <div className="relative w-24 h-24 sm:w-28 sm:h-28">
          <div
            className={`absolute inset-0 rounded-full bg-gradient-to-br ${scoreColor} blur-lg opacity-30`}
          />
          <div className="relative flex items-center justify-center w-full h-full rounded-full bg-white shadow-lg">
            <span className="text-2xl sm:text-3xl font-bold text-gray-800">
              {avgMatch}
            </span>
            <span className="text-xs text-gray-500 ml-1">/100</span>
          </div>
          <p className="text-xs text-center mt-2 text-gray-500">
            Resume Score
          </p>
        </div>
      </div>

      {/* EXTRACTED SKILLS */}
      <div className="mb-8 sm:mb-10">
        <h3 className="text-lg font-semibold mb-3 flex items-center justify-center sm:justify-start gap-2">
          <CheckCircle2 className="w-5 h-5 text-green-600" />
          Strengths Identified
        </h3>

        <div className="flex flex-wrap justify-center sm:justify-start gap-2 sm:gap-3">
          {result.extracted_skills.map((skill, i) => (
            <span
              key={i}
              className="bg-gradient-to-r from-green-100 to-green-200 text-green-800 px-3 py-1 sm:px-4 sm:py-2 rounded-full text-xs sm:text-sm font-semibold shadow-sm"
            >
              {skill}
            </span>
          ))}
        </div>
      </div>

      {/* CAREER MATCHES */}
      <div>
        <h3 className="text-lg font-semibold mb-5 flex items-center justify-center sm:justify-start gap-2">
          <Award className="w-5 h-5 text-blue-600" />
          Career Fit Analysis
        </h3>

        <div className="space-y-4 sm:space-y-6">
          {result.top_recommendations.map((rec, i) => {
            const tier =
              rec.match_percentage >= 75
                ? "Excellent Fit"
                : rec.match_percentage >= 55
                ? "Good Potential"
                : "Needs Upskilling";

            const tierColor =
              rec.match_percentage >= 75
                ? "text-green-600"
                : rec.match_percentage >= 55
                ? "text-yellow-600"
                : "text-red-600";

            return (
              <div
                key={i}
                className="bg-white rounded-2xl border p-4 sm:p-6 shadow-sm hover:shadow-lg transition"
              >
                {/* ROLE HEADER */}
                <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-3 gap-2 sm:gap-0">
                  <div>
                    <p className="text-lg sm:text-xl font-bold text-gray-800">
                      {rec.role}
                    </p>
                    <p className={`text-xs sm:text-sm font-medium ${tierColor}`}>
                      {tier}
                    </p>
                  </div>

                  <div className="text-right mt-1 sm:mt-0">
                    <p className="text-xl sm:text-2xl font-bold text-gray-800">
                      {rec.match_percentage}%
                    </p>
                    <p className="text-xs text-gray-500">Match</p>
                  </div>
                </div>

                {/* PROGRESS */}
                <div className="w-full bg-gray-200 rounded-full h-2 mb-3 sm:mb-4">
                  <div
                    className={`h-2 rounded-full bg-gradient-to-r ${
                      rec.match_percentage >= 75
                        ? "from-green-500 to-emerald-500"
                        : rec.match_percentage >= 55
                        ? "from-yellow-400 to-orange-500"
                        : "from-red-400 to-pink-500"
                    }`}
                    style={{ width: `${rec.match_percentage}%` }}
                  />
                </div>

                {/* GAP */}
                {rec.missing_skills.length > 0 ? (
                  <div className="bg-red-50 border border-red-100 rounded-xl p-3 sm:p-4 text-xs sm:text-sm">
                    <div className="flex items-center gap-1 sm:gap-2 text-red-600 mb-1 sm:mb-2">
                      <AlertTriangle className="w-3 h-3 sm:w-4 sm:h-4" />
                      <span className="font-semibold">Skill Gaps to Focus On</span>
                    </div>
                    <p className="text-red-700">
                      {rec.missing_skills.slice(0, 6).join(", ")}
                    </p>

                    {rec.missing_skills.length > 6 && (
                      <p className="text-red-700 mt-1 sm:mt-2 text-xs sm:text-sm">
                        and {rec.missing_skills.length - 6} more...
                      </p>
                    )}
                  </div>
                ) : (
                  <div className="flex items-center gap-1 sm:gap-2 text-green-600 font-semibold text-xs sm:text-sm">
                    <TrendingUp className="w-3 h-3 sm:w-4 sm:h-4" />
                    You are fully aligned with this role
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
