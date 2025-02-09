import React, { useState } from 'react';
import { Eye, ChevronLeft, ChevronRight, Send, LogIn, Database, Play, School as Schema, Award, Timer } from 'lucide-react';

interface Question {
  id: number;
  text: string;
  schema?: string;
}

const questions: Question[] = [
  { 
    id: 1, 
    text: "Get all participants with score above 80.",
    schema: `Table participants {
  id INT [pk]
  name VARCHAR
  score INT
  created_at TIMESTAMP
}`
  },
  { 
    id: 2, 
    text: "Find the highest score in the participants table.",
    schema: `Table participants {
  id INT [pk]
  name VARCHAR
  score INT
  created_at TIMESTAMP
}`
  },
  { 
    id: 3, 
    text: "Retrieve all users sorted by score in descending order.",
    schema: `Table participants {
  id INT [pk]
  name VARCHAR
  score INT
  created_at TIMESTAMP
}`
  },
  { id: 4, text: "Find the total number of participants." },
  { id: 5, text: "Select all participants whose name starts with 'A'." },
  { id: 6, text: "Get the second highest score from the table." },
  { id: 7, text: "Find participants with the lowest score." },
  { id: 8, text: "Count the number of unique scores." },
  { id: 9, text: "Retrieve all participants who scored 90 or above." },
  { id: 10, text: "Get the average score of all participants." }
];

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [query, setQuery] = useState('');
  const [output, setOutput] = useState('');
  const [submittedQuestions, setSubmittedQuestions] = useState(new Set<number>());
  const [isExecuting, setIsExecuting] = useState(false);
  const [showSchema, setShowSchema] = useState(false);
  const [timeLeft, setTimeLeft] = useState(3600); // 1 hour in seconds

  React.useEffect(() => {
    if (isLoggedIn) {
      const timer = setInterval(() => {
        setTimeLeft((prev) => Math.max(0, prev - 1));
      }, 1000);
      return () => clearInterval(timer);
    }
  }, [isLoggedIn]);

  const formatTime = (seconds: number) => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
  };

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    // In a real app, this would make an API call to validate credentials
    setIsLoggedIn(true);
  };

  const handleSubmitQuery = async () => {
    setIsExecuting(true);
    try {
      // Simulated API call with delay
      await new Promise(resolve => setTimeout(resolve, 1000));
      const newSubmitted = new Set(submittedQuestions);
      newSubmitted.add(currentQuestionIndex);
      setSubmittedQuestions(newSubmitted);
      setOutput('Query submitted successfully!');
    } finally {
      setIsExecuting(false);
    }
  };

  const handleViewOutput = async () => {
    setIsExecuting(true);
    try {
      // Simulated API call with delay
      await new Promise(resolve => setTimeout(resolve, 800));
      setOutput('SELECT * FROM participants WHERE score > 80;\n\n[{"id": 1, "name": "John", "score": 85},\n{"id": 2, "name": "Alice", "score": 92}]');
    } finally {
      setIsExecuting(false);
    }
  };

  if (!isLoggedIn) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-900 to-indigo-900 flex items-center justify-center p-4">
        <div className="bg-white/95 backdrop-blur-sm rounded-xl shadow-2xl p-8 w-full max-w-md">
          <div className="flex items-center justify-center mb-6">
            <Database className="w-12 h-12 text-indigo-600" />
          </div>
          <h2 className="text-3xl font-bold text-gray-800 mb-2 text-center">DATABASE DESIGN DUEL</h2>
          <p className="text-center text-gray-600 mb-6">by Intellexa</p>
          <form onSubmit={handleLogin} className="space-y-4">
            <div>
              <label htmlFor="username" className="block text-sm font-medium text-gray-700 mb-1">
                Username
              </label>
              <input
                type="text"
                id="username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                required
              />
            </div>
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
                Password
              </label>
              <input
                type="password"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                required
              />
            </div>
            <button
              type="submit"
              className="w-full bg-indigo-600 text-white py-3 px-4 rounded-lg hover:bg-indigo-700 transition-colors flex items-center justify-center gap-2"
            >
              <LogIn size={20} />
              Enter the Arena
            </button>
          </form>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 to-indigo-900 p-4 sm:p-6 lg:p-8">
      <div className="max-w-5xl mx-auto">
        <div className="flex items-center justify-between mb-6 bg-white/10 backdrop-blur-sm rounded-lg p-4 text-white">
          <div className="flex items-center gap-3">
            <Database className="w-6 h-6" />
            <h1 className="text-xl font-bold">DATABASE DESIGN DUEL</h1>
          </div>
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2">
              <Timer className="w-5 h-5" />
              <span className="font-mono">{formatTime(timeLeft)}</span>
            </div>
            <div className="flex items-center gap-2">
              <Award className="w-5 h-5" />
              <span>Score: {submittedQuestions.size * 10}</span>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-xl p-6">
          <div className="mb-6">
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-semibold text-gray-800">
                Question {questions[currentQuestionIndex].id} of {questions.length}
              </h2>
              {questions[currentQuestionIndex].schema && (
                <button
                  onClick={() => setShowSchema(!showSchema)}
                  className="flex items-center gap-2 px-4 py-2 text-indigo-600 hover:bg-indigo-50 rounded-lg transition-colors"
                >
                  <Schema size={20} />
                  {showSchema ? 'Hide Schema' : 'Show Schema'}
                </button>
              )}
            </div>
            <p className="text-gray-600 mt-2">{questions[currentQuestionIndex].text}</p>
            {showSchema && questions[currentQuestionIndex].schema && (
              <div className="mt-4 p-4 bg-gray-50 rounded-lg border border-gray-200">
                <pre className="text-sm font-mono text-gray-700">{questions[currentQuestionIndex].schema}</pre>
              </div>
            )}
          </div>

          <div className="space-y-4">
            <div>
              <label htmlFor="query" className="block text-sm font-medium text-gray-700 mb-1">
                Your SQL Query
              </label>
              <textarea
                id="query"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                className="w-full h-32 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 font-mono"
                placeholder="Write your SQL query here..."
              />
            </div>

            <div className="flex flex-wrap gap-3">
              <button
                onClick={() => setCurrentQuestionIndex(Math.max(0, currentQuestionIndex - 1))}
                disabled={currentQuestionIndex === 0}
                className="flex items-center gap-1 px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <ChevronLeft size={20} />
                Previous
              </button>

              <button
                onClick={handleSubmitQuery}
                disabled={submittedQuestions.has(currentQuestionIndex) || isExecuting}
                className="flex items-center gap-1 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isExecuting ? (
                  <div className="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent" />
                ) : (
                  <Send size={20} />
                )}
                Submit
              </button>

              <button
                onClick={handleViewOutput}
                disabled={isExecuting}
                className="flex items-center gap-1 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isExecuting ? (
                  <div className="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent" />
                ) : (
                  <Play size={20} />
                )}
                Execute
              </button>

              <button
                onClick={() => setCurrentQuestionIndex(Math.min(questions.length - 1, currentQuestionIndex + 1))}
                disabled={currentQuestionIndex === questions.length - 1}
                className="flex items-center gap-1 px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Next
                <ChevronRight size={20} />
              </button>
            </div>

            {output && (
              <div className="mt-6 animate-fade-in">
                <h3 className="text-sm font-medium text-gray-700 mb-2">Query Output</h3>
                <pre className="bg-gray-50 p-4 rounded-lg overflow-x-auto font-mono text-sm border border-gray-200">
                  {output}
                </pre>
              </div>
            )}
          </div>

          <div className="mt-6 pt-6 border-t border-gray-200">
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-500">
                Logged in as <span className="font-medium">{username}</span>
              </span>
              <div className="flex items-center gap-2">
                <span className="text-sm text-gray-500">
                  Progress: {submittedQuestions.size} / {questions.length}
                </span>
                <div className="w-32 h-2 bg-gray-200 rounded-full overflow-hidden">
                  <div 
                    className="h-full bg-indigo-600 transition-all duration-300"
                    style={{ width: `${(submittedQuestions.size / questions.length) * 100}%` }}
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;