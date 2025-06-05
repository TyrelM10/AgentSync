import { motion } from 'framer-motion';
import InputField from './InputField';
import TextArea from './TextArea';

interface ToolCardProps {
  title: string;
  description: string;
  children: React.ReactNode;
  onSubmit: (e: React.FormEvent<HTMLFormElement>) => void;
  isLoading: boolean;
}

const ToolCard = ({ title, description, children, onSubmit, isLoading }: ToolCardProps) => {
  return (
    <motion.div
      className="p-4 bg-gray-800/50 backdrop-blur-lg rounded-xl border border-blue-700/30 shadow-lg hover:shadow-blue-700/20 transition-shadow"
      whileHover={{ scale: 1.01 }}
      transition={{ type: 'spring', stiffness: 300 }}
    >
      <h2 className="text-lg font-bold text-blue-400 mb-1 font-orbitron">{title}</h2>
      <p className="text-sm text-gray-300 mb-2">{description}</p>
      <form onSubmit={onSubmit} className="space-y-2">
        {children}
        <button
          type="submit"
          disabled={isLoading}
          className="w-full bg-blue-800 text-white py-2 px-3 rounded-lg glow-blue disabled:opacity-50 hover:bg-blue-900 transition-all flex items-center justify-center text-sm"
        >
          {isLoading ? (
            <svg
              className="animate-spin h-4 w-4 mr-2 text-white"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
              ></circle>
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              ></path>
            </svg>
          ) : null}
          {isLoading ? 'Processing...' : 'Execute'}
        </button>
      </form>
    </motion.div>
  );
};

export default ToolCard;