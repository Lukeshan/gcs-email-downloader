import React from "react";

interface DropdownProps {
  options: string[];
  selectedValue: string;
  isVisible:boolean;
  setSelectedValue: (value: string) => void;
}

const Dropdown: React.FC<DropdownProps> = ({ options, selectedValue, setSelectedValue }) => {
  const handleSelect = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedValue(event.target.value);
  };

  return (
    <div className="flex flex-col items-center">
      <label className="text-lg font-medium mb-2">Choose an option:</label>
      <select
        onChange={handleSelect}
        value={selectedValue}
        className="w-64 px-4 py-2 border border-neutral-700 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 bg-neutral-700 text-shadow-white"
      >
        <option value="" disabled>Select an option</option>
        {options.map((option, index) => (
          <option key={index} value={option}>{option}</option>
        ))}
      </select>
    </div>
  );
};

export default Dropdown;
