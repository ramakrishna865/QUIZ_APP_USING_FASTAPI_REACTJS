
import React, { useEffect, useState, useRef } from "react";
import "./quizapp.css";

function QuizApp() {
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState({});
  const [status, setStatus] = useState({});
  const [errors, setErrors] = useState({});
  const [userInfo, setUserInfo] = useState({ name: "", email: "" });
  const [result, setResult] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [timer, setTimer] = useState(90);
  const inputRef = useRef(null);

  useEffect(() => {
    fetch("http://192.168.100.87:8000/categories/")
      .then((res) => res.json())
      .then((data) => setCategories(data))
      .catch(() => alert("Failed to load categories"));
  }, []);

  useEffect(() => {
    if (!selectedCategory) return;
    fetch(`http://192.168.100.87:8000/questions/?category_id=${selectedCategory}`)
      .then((res) => res.json())
      .then((data) => {
        if (data.length === 0) {
          alert("No questions available.");
          setSelectedCategory(null);
          return;
        }
        setQuestions(data);
        setAnswers({});
        setStatus(Object.fromEntries(data.map((q) => [q.id, "not_visited"])));
        setErrors({});
        setCurrentQuestionIndex(0);
        setResult(null);
        setUserInfo({ name: "", email: "" });
        setShowModal(false);
        setTimer(90);
      });
  }, [selectedCategory]);

  useEffect(() => {
    if (questions.length === 0 || result) return;
    const interval = setInterval(() => {
      setTimer((prev) => {
        if (prev <= 1) {
          clearInterval(interval);
          submitQuiz();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
    return () => clearInterval(interval);
  }, [questions, result]);

  const currentQuestion = questions[currentQuestionIndex];
  const currentAnswer = answers[currentQuestion?.id] || "";

  // const validateAnswer = (q, value) => {
  //   if (!value) return "Answer is required.";
  //   if (q.type_mandatory === "mandatory") {
  //     if (q.type === "numeric" && isNaN(value)) return "Expected numeric value.";
  //     if (q.type === "boolean" && !["true", "false"].includes(value)) return "Expected true or false.";
  //     if (q.type === "string" && !isNaN(value)) return "Expected string value.";
  //   }
  //   if (q.min_limit_mandatory === "mandatory" && value.length < q.min_limit)
  //     return `Minimum ${q.min_limit} characters required.`;
  //   if (q.max_limit_mandatory === "mandatory" && value.length > q.max_limit)
  //     return `Maximum ${q.max_limit} characters allowed.`;
  //   return "";
  // };
const validateAnswer = (q, value) => {
  if (!value) return "Answer is required.";

  if (q.type_mandatory === "mandatory") {
    if (q.type === "numeric" && isNaN(value)) return "Expected numeric value.";
    if (q.type === "boolean" && !["true", "false"].includes(value.toLowerCase())) return "Expected true or false.";
    if (q.type === "string" && !isNaN(value)) return "Expected string value.";
  }

  if (q.min_limit_mandatory === "mandatory" && value.length < q.min_limit)
    return `Minimum ${q.min_limit} characters required.`;

  if (q.max_limit_mandatory === "mandatory" && value.length > q.max_limit)
    return `Maximum ${q.max_limit} characters allowed.`;

  return "";
};

  // const handleAnswerChange = (value) => {
  //   if (
  //     currentQuestion.max_limit_mandatory === "mandatory" &&
  //     value.length > currentQuestion.max_limit
  //   ) {
  //     return;
  //   }
  //   setAnswers((prev) => ({ ...prev, [currentQuestion.id]: value }));
  //   setErrors((prev) => ({ ...prev, [currentQuestion.id]: "" }));
  // };
  const handleAnswerChange = (value) => {
  if (!currentQuestion) return;

  const { type, type_mandatory, min_limit, max_limit, min_limit_mandatory, max_limit_mandatory } = currentQuestion;

  // Apply character length constraints
  if (max_limit_mandatory === "mandatory" && value.length > max_limit) {
    return; // prevent typing beyond max length
  }

  // Type checks
  if (type_mandatory === "mandatory") {
    if (type === "numeric" && value && !/^\d*\.?\d*$/.test(value)) return;
    if (type === "string" && /\d/.test(value)) return; // block if numeric in mandatory string
  }

  setAnswers((prev) => ({ ...prev, [currentQuestion.id]: value }));
  setErrors((prev) => ({ ...prev, [currentQuestion.id]: "" }));
};


  

  const saveAnswer = () => {
    const error = validateAnswer(currentQuestion, currentAnswer);
    if (error) {
      setErrors((prev) => ({ ...prev, [currentQuestion.id]: error }));
      return;
    }
    setStatus((prev) => ({ ...prev, [currentQuestion.id]: "saved" }));
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
    }
  };

  const markForReview = () => {
    setStatus((prev) => ({ ...prev, [currentQuestion.id]: "marked" }));
  };

  const handleUserInfoChange = (e) => {
    const { name, value } = e.target;
    setUserInfo((prev) => ({ ...prev, [name]: value }));
  };

  const getFeedbackMessage = (score, total) => {
    const percent = (score / total) * 100;
    if (percent === 100) return { msg: "🎉 Congratulations! Perfect Score!", emoji: "🏆" };
    if (percent >= 70) return { msg: "👏 Great Job! You're close!", emoji: "😃" };
    if (percent >= 50) return { msg: "😐 Not bad, try harder next time!", emoji: "🙂" };
    return { msg: "😢 Very low score. Better luck next time!", emoji: "💔" };
  };

  const submitQuiz = () => {
    if (!userInfo.name || !userInfo.email) {
      alert("Please enter your name and email before submitting.");
      return;
    }
    const unanswered = questions.some((q) => status[q.id] !== "saved");
    if (unanswered) {
      const first = questions.findIndex((q) => status[q.id] !== "saved");
      setCurrentQuestionIndex(first);
      setErrors((prev) => ({ ...prev, [questions[first].id]: "Please answer this." }));
      return;
    }
    const payload = {
      name: userInfo.name,
      email: userInfo.email,
      answers: questions.map((q) => ({ question_id: q.id, answer: answers[q.id] })),
    };
    fetch("http://192.168.100.87:8000/submit/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    })
      .then((res) => res.json())
      .then((data) => {
        const correctIds = questions
          .filter((q) => q.answer?.toLowerCase().trim() === (answers[q.id] || "").toLowerCase().trim())
          .map((q) => q.id);

        const score = questions.reduce((acc, q) => {
          if (!answers[q.id]) return acc;
          if (correctIds.includes(q.id)) return acc + 3;
          return acc - 1;
        }, 0);

        setResult({ ...data, correctIds, score, total: questions.length * 3 });
        setShowModal(true);
      });
  };

  return (
    <div className="quiz-container">
      <h1>📚 Quiz Application</h1>

      <div className="category-bar">
        {categories.map((cat) => (
          <button
            key={cat.id}
            onClick={() => setSelectedCategory(cat.id)}
            className={`category-btn ${selectedCategory === cat.id ? "selected" : ""}`}
          >
            {cat.name}
          </button>
        ))}
      </div>

      {questions.length > 0 && (
        <>
          <div className="timer-display">⏱️ Time Left: {timer}s</div>
          <div className="navigation-panel">
            {questions.map((q, i) => (
              <button
                key={q.id}
                onClick={() => setCurrentQuestionIndex(i)}
                className={`nav-btn ${status[q.id]}`}
              >
                {i + 1}
              </button>
            ))}
          </div>

          <div className="question-section" ref={inputRef}>
            <p><strong>Q{currentQuestionIndex + 1}:</strong> {currentQuestion.question}</p>

            <div className="note">
              {currentQuestion.min_limit_mandatory === "mandatory" && (
                <p>* Min characters should be {currentQuestion.min_limit}</p>
              )}
              {currentQuestion.max_limit_mandatory === "mandatory" && (
                <p>* Max characters should be {currentQuestion.max_limit}</p>
              )}
              {currentQuestion.type_mandatory === "mandatory" && (
                <p>* The answer must be in {currentQuestion.type}</p>
              )}
            </div>

            {currentQuestion.type === "boolean" ? (
              <div className="radio-group">
                {["true", "false"].map((val) => (
                  <label className="radio-option" key={val}>
                    <input
                      type="radio"
                      name={`bool-${currentQuestion.id}`}
                      checked={currentAnswer === val}
                      onChange={() => handleAnswerChange(val)}
                    />
                    {val.charAt(0).toUpperCase() + val.slice(1)}
                  </label>
                ))}
              </div>
            ) : (
              <input
                type="text"
                value={currentAnswer}
                onChange={(e) => handleAnswerChange(e.target.value)}
              />
            )}

            {errors[currentQuestion?.id] && <p className="error-msg">{errors[currentQuestion.id]}</p>}

            <div className="action-buttons">
              <button onClick={saveAnswer}>Save & Next</button>
              <button onClick={markForReview}>Mark for Review</button>
            </div>
          </div>

          <div className="submit-section">
            <h3>Enter your details:</h3>
            <input
              type="text"
              name="name"
              placeholder="Your Name"
              value={userInfo.name}
              onChange={handleUserInfoChange}
            />
            <input
              type="email"
              name="email"
              placeholder="Your Email"
              value={userInfo.email}
              onChange={handleUserInfoChange}
            />
            <button className="submit-btn" onClick={submitQuiz}>Submit Quiz</button>
          </div>

          {showModal && result && (
            <div className="modal-overlay">
              <div className="modal-content">
                <h2>📊 Result</h2>
                <p>Score: {result.score} / {result.total}</p>
                <p>{getFeedbackMessage(result.score, result.total).emoji} {getFeedbackMessage(result.score, result.total).msg}</p>
                <hr />
                <div className="result-summary">
                  {questions.map((q, i) => {
                    const userAns = answers[q.id];
                    const correct = result.correctIds.includes(q.id);
                    return (
                      <div key={q.id} className={correct ? "correct" : "incorrect"}>
                        <p><strong>Q{i + 1}:</strong> {q.question} {correct ? "✔️" : "✖️"}</p>
                        <p><span className="label">Your Answer:</span> {userAns}</p>
                        {!correct && <p><span className="label">Correct Answer:</span> {q.answer}</p>}
                      </div>
                    );
                  })}
                </div>
                <button className="submit-btn" onClick={() => setShowModal(false)}>Close</button>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}

export default QuizApp;
