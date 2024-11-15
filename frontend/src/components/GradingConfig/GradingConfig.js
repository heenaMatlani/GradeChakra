import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './GradingConfig.css'; // Import the CSS file

const GradingConfig = () => {
  const [isUsingJson, setIsUsingJson] = useState(false); // Toggle for JSON input
  const [gradingType, setGradingType] = useState('special'); // Default grading type
  const [maxScore, setMaxScore] = useState('');
  const [useBestNofM, setUseBestNofM] = useState(false);
  const [nValue, setNValue] = useState(0);
  const [mValue, setMValue] = useState(0);
  const [yearRepetition, setYearRepetition] = useState('');
  const [yearRepetitionDisplay, setYearRepetitionDisplay] = useState('');
  const [courseRepeat, setCourseRepeat] = useState('');
  const [labCourseRepeat, setLabCourseRepeat] = useState('');
  const [courseRepeatAndSupplementaryDisplay, setCourseRepeatAndSupplementaryDisplay] = useState('');
  const [spiFormula, setSpiFormula] = useState('default_spi_formula');
  const [spiName, setSpiName] = useState('');
  const [cpiName, setCpiName] = useState('');
  const [batchYear, setBatchYear] = useState(2021);
  const [rules, setRules] = useState({});
  const [courseRepeatAndSupplementaryDisplayDescription, setCourseRepeatAndSupplementaryDisplayDescription] = useState('');
  const [labCourseRepeatDescription, setLabCourseRepeatDescription] = useState('');
  const [courseRepeatDescription, setCourseRepeatDescription] = useState('');
  const [yearRepetitionDisplayDescription, setYearRepetitionDisplayDescription] = useState('');
  const [yearRepetitionDescription, setYearRepetitionDescription] = useState('');
  const [decimalPlaces, setDecimalPlaces] = useState(2); // Round off limit, default to 2
  const [error, setError] = useState(null); // Error state for validation feedback

  useEffect(() => {
    const fetchRules = async () => {
      try {
        const response = await axios.get('/fetch-rules');
        setRules(response.data);
      } catch (error) {
        console.error("Error fetching rules:", error);
      }
    };

    fetchRules();
  }, []);

    const isAlphabetical = (obj) => {
    const keys = Object.keys(obj);
    return keys.every((key, i) => i === 0 || key >= keys[i - 1]);
  };

  const validateGradesFormat = (grades) => {
    if (!isAlphabetical(grades)) {
      return "Keys in 'grades' should be in alphabetical order.";
    }
    for (const [key, value] of Object.entries(grades)) {
      if (typeof key !== 'string' || !/^[A-Za-z]+$/.test(key)) {
        return "Keys in 'grades' should be alphabetical.";
      }
      if (typeof value !== 'number' || isNaN(value)) {
        return "Values in 'grades' should be numbers.";
      }
    }
    return null;
  };

   const validateJsonInput = (jsonInput) => {
    const errors = [];

    // Validate grading_system fields
    if (!jsonInput.grading_system) {
      errors.push("Missing 'grading_system' field");
    } else {
      const gradingSystem = jsonInput.grading_system;

      if (!gradingSystem.type || !['special', 'numeric'].includes(gradingSystem.type)) {
        errors.push("Invalid or missing 'type' in 'grading_system'. Must be 'special' or 'numeric'");
      }
      if (!gradingSystem.max_score || isNaN(gradingSystem.max_score)) {
        errors.push("Invalid or missing 'max_score'. Must be a number");
      }
      if (gradingSystem.type === 'special') {
        if (!gradingSystem.grades) {
          errors.push("'grades' is required when 'type' is 'special'.");
        } else {
          const gradesError = validateGradesFormat(gradingSystem.grades);
          if (gradesError) errors.push(gradesError);
        }
      }

    if (gradingSystem.use_best_n_of_m) {
        console.log(gradingSystem.use_best_n_of_m)
        const useBestFormat = /use_best_(\d+)_of_(\d+)/;
        const match = useBestFormat.exec(gradingSystem.use_best_n_of_m);

        if (!match) {
            errors.push("Invalid format for 'use_best_n_of_m'. Expected format: 'use_best_X_of_Y'.");
        } else {
            const n = parseInt(match[1], 10);
            const m = parseInt(match[2], 10);

            if (isNaN(n) || isNaN(m) || n >= m) {
                errors.push("'best_n' must be a number less than 'total_m' in 'use_best_n_of_m'.");
            }
        }
    }
    }

    // Validate policy fields
  const requiredPolicies = ["year_repetition", "course_repeat", "lab_course_repeat", "course_repeat_and_supplementary_display"];
  requiredPolicies.forEach(policy => {
    if (!jsonInput[policy]) {
      errors.push(`Missing '${policy}' field`);
    } else {
      if (policy === "year_repetition" ){
        if (!rules[`${policy}_rules`]?.some(rule => rule.rule_name === jsonInput[policy].rule)) {
          console.log(jsonInput[policy])
          errors.push(`Invalid value for '${policy}'`);
        }
        if (!rules[`display_options`]?.some(option => option.option_name === jsonInput[policy].display)) {
          errors.push(`Invalid value for '${policy}'`);
        }
      }
      else if ( policy === "course_repeat" || policy === "lab_course_repeat") {
        // These should be matched with rule_name
        if (policy == "lab_course_repeat"){
        policy = "course_repeat"
        }
        if (!rules[`${policy}_rules`]?.some(rule => rule.rule_name === jsonInput[policy])) {
          console.log(jsonInput[policy])
          errors.push(`Invalid value for '${policy}'`);
        }
      } else if (policy === "spi_formula") {
      // Validate SPI formula against the database values
        if (!rules[`spi_formulas`]?.some(option => option.formula_name === jsonInput[policy])) {
          errors.push(`Invalid value for '${policy}'`);
        }
    } else {
        // These should be matched with option_name (display options)
        if (!rules[`display_options`]?.some(option => option.option_name === jsonInput[policy])) {
          errors.push(`Invalid value for '${policy}'`);
        }
      }
    }
  });

    // Validate SPI/CPI details
    if (!jsonInput.spi_name || !jsonInput.cpi_name) {
      errors.push("Both 'spi_name' and 'cpi_name' are required");
    }
    if (!jsonInput.round_to_decimal_places || isNaN(jsonInput.round_to_decimal_places) || jsonInput.round_to_decimal_places < 0) {
      errors.push("'round_to_decimal_places' must be a positive integer");
    }

    return errors.length ? errors : null;
  };

  const handleJsonSubmit = async () => {
    let parsedJson;
    try {
      parsedJson = JSON.parse(gradingSystemJson);
    } catch (err) {
      setError("Invalid JSON format. Please check your input.");
      alert(error);
      return;
    }

    const validationErrors = validateJsonInput(parsedJson);
    if (validationErrors) {
      setError(validationErrors.join(", "));
      alert(error);
      return;
    }

    setError(null); // Clear previous errors if validation passes
    try {
      await axios.post('/set-grading-rules', parsedJson);
      alert("Grading system (JSON) updated successfully");
    } catch (error) {
      console.error("Error setting grading rules:", error);
      setError("Failed to submit grading configuration. Please try again.");
      alert(error);
    }
  };

  const handleFilledBoxSubmit = async () => {

    let parsedGrades = null;

    // Only validate grades if gradingType is "special"
    if (gradingType === 'special') {
        try {
            parsedGrades = JSON.parse(gradesJson);
        } catch (err) {
            setError("Invalid 'grades' format. Must be a valid JSON object.");
            return;
        }

        const gradesError = validateGradesFormat(parsedGrades);
        if (gradesError) {
            setError(gradesError);
            return;
        }
    }

    // Ensure max_score is provided and is numeric
    if (!maxScore || isNaN(maxScore)) {
        setError("Please enter a valid numeric value for 'Max Score'.");
        return;
    }
    let useBestNofMValue = useBestNofM ? `use_best_${nValue}_of_${mValue}` : null;

    // Check for N < M condition if useBestNofM is true
    if (useBestNofM && (parseInt(nValue) >= parseInt(mValue) || isNaN(nValue) || isNaN(mValue))) {
        setError("For 'Use Best N of M', ensure that 'N' is less than 'M' and both are valid numbers.");
        return;
    }
    const gradingConfig = {
      grading_system: {
        type: gradingType,
        grades: gradingType === 'special' ? JSON.parse(gradesJson) : null,
        max_score: parseFloat(maxScore),
        use_best_n_of_m: useBestNofMValue,

      },
      year_repetition: { rule: yearRepetition , display: yearRepetitionDisplay},
      course_repeat_and_supplementary_display: courseRepeatAndSupplementaryDisplay,
      course_repeat: courseRepeat,
      lab_course_repeat: labCourseRepeat,
      spi_formula: spiFormula,
      spi_name: spiName,
      cpi_name: cpiName,
      round_to_decimal_places: parseInt(decimalPlaces),
      start_batch_year: parseInt(batchYear)
    };

    try {
      await axios.post('/set-grading-rules', gradingConfig);
      alert("Grading system updated successfully");
    } catch (error) {
      console.error("Error setting grading rules:", error);
      setError("Failed to submit grading configuration. Please try again.");
    }
  };

  const handleSubmit = () => {
    if (isUsingJson) {
      handleJsonSubmit();
    } else {
      handleFilledBoxSubmit();
    }
  };
  // JSON for grading system
  const sampleGradingSystemJson = JSON.stringify({
    "grading_system": {
      "type": "special",
      "grades": {
        "AA": 10,
        "AB": 9,
        "BB": 8,
        "BC": 7,
        "CC": 6,
        "CD": 5,
        "DD": 4,
        "F": 0
      },
      "max_score": 10.0,
      "use_best_n_of_m": "use_best_5_of_7",
    },
    "year_repetition": {
      "rule": "reset_previous_results",
      "display": "show_previous_results_with_asterisk"
    },
    "course_repeat": "replace_with_higher_grade",
    "lab_course_repeat": "average_of_grades",
    "course_repeat_and_supplementary_display": "show_previous_results_with_asterisk",
    "spi_formula": "default_spi_formula",
    "spi_name": "SPI",
    "cpi_name": "CPI",
    "round_to_decimal_places": 2,
    "start_batch_year": 2018
  }, null, 2);

  const sampleGradesJson = JSON.stringify({
        "AA": 10,
        "AB": 9,
        "BB": 8,
        "BC": 7,
        "CC": 6,
        "CD": 5,
        "DD": 4,
        "F": 0
      }, null, 2);
  const [gradesJson, setGradesJson] = useState(sampleGradesJson); // Initialize JSON
  const [gradingSystemJson, setGradingSystemJson] = useState(sampleGradingSystemJson); // Initialize JSON

  const getInfoTooltip = (label) => {
    const tooltips = {
      "Grading Type": "numeric: Numbers (e.g., 90) or special: Custom grades (e.g., A, B, AA).",
      "Max Score": "Integer or float representing highest grade value (e.g., 10 for 10-point scale).",
      "Use Best N of M": "Select best N out of M subjects for calculation (e.g., use_best_5_of_7).",
      "Year Repetition": "Reset all grades or keep previous grades, depending on the option selected.",
      "Year Repetition Display": "Choose how repeated grades after year repetition are displayed.",
      "Course Repeat Policy": "Defines the rule for replacing grades upon course repeat.",
      "Lab Course Repeat": "Defines the rule for replacing grades upon lab course repeat.",
      "Course Repeat & Supplementary Display": "Choose how repeated grades are displayed.",
      "SPI Formula": "Default or custom formula to calculate SPI (Semester Performance Index).",
      "SPI Name": "Define the name for semester index (e.g., SPI or SGPA).",
      "CPI Name": "Define the name for cumulative index (e.g., CPI or CGPA).",
      "Batch Year": "The batch year from which the grading system will be implemented.",
    };
    return tooltips[label];
  };
  const handleSelectChange = (value, options, setState, setDescriptionState) => {
    setState(value);
    const selectedOption = options.find((option) => option.rule_name === value || option.option_name === value);
    setDescriptionState(selectedOption ? selectedOption.description : '');
  };



  return (

    <div className="grading-config-container">
      <h2>Grading System Configuration</h2>

      {/* Toggle for JSON or Filled Boxes */}
      <div className="grading-config-toggle-switch">
        <div className={`grading-config-toggle-btn ${!isUsingJson ? 'active' : ''}`} onClick={() => setIsUsingJson(false)}>
          Filled Boxes
        </div>
        <div className={`grading-config-toggle-btn ${isUsingJson ? 'active' : ''}`} onClick={() => setIsUsingJson(true)}>
          Use JSON
        </div>
      </div>

      {/* Conditional rendering for filled boxes */}
      {!isUsingJson && (
        <div>
          {/* Grading Type Dropdown */}
          <label>
            Grading Type
            <i className="info-icon fas fa-info-circle" title={getInfoTooltip("Grading Type")}></i>
          </label>
          <select value={gradingType} onChange={(e) => setGradingType(e.target.value)}>
            <option value="numeric">Numeric</option>
            <option value="special">Special</option>
          </select>

          {/* Conditional rendering for special grades JSON input */}
          {gradingType === 'special' && (
            <div>
              <label>Grades (JSON format):</label>
              <textarea
                className="grades-json-text-area"
                rows="5"
                value={gradesJson}
                onChange={(e) => setGradesJson(e.target.value)}
              />
            </div>
          )}

          {/* Max Score Input */}
          <label>
            Max Score
            <i className="info-icon fas fa-info-circle" title={getInfoTooltip("Max Score")}></i>
          </label>          <input
            type="number"
            value={maxScore}
            onChange={(e) => setMaxScore(e.target.value)}
            min="1"
          />

          {/* Use Best N of M */}
          <label>
            Use Best N of M
            <i className="info-icon fas fa-info-circle" title={getInfoTooltip("Use Best N of M")}></i>
          </label>          <select onChange={(e) => setUseBestNofM(e.target.value === 'yes')}>
            <option value="no">No</option>
            <option value="yes">Yes</option>
          </select>

          {useBestNofM && (
            <div>
              <label>N:</label>
              <input
                type="number"
                value={nValue}
                onChange={(e) => setNValue(e.target.value)}
              />
              <label>M:</label>
              <input
                type="number"
                value={mValue}
                onChange={(e) => setMValue(e.target.value)}
              />
            </div>
          )}


      {/* Year Repetition */}
      <div className="field-group">
        <label>
          Year Repetition
          <i className="info-icon fas fa-info-circle" title={getInfoTooltip("Year Repetition")}></i>
        </label>
        <select
          value={yearRepetition}
          onChange={(e) => handleSelectChange(e.target.value, rules.year_repetition_rules, setYearRepetition, setYearRepetitionDescription)}
        >
          <option value="">Select a policy</option>
          {rules.year_repetition_rules?.map((rule) => (
            <option key={rule.rule_name} value={rule.rule_name}>
              {rule.rule_name}
            </option>
          ))}
        </select>
        {yearRepetitionDescription && (
          <p className="description-text">
            <i className="info-icon fas fa-info-circle"></i> {yearRepetitionDescription}
          </p>
        )}
      </div>

      {/* Year Repetition Display */}
      <div className="field-group">
        <label>
          Year Repetition Display
          <i className="info-icon fas fa-info-circle" title={getInfoTooltip("Year Repetition Display")}></i>
        </label>
        <select
          value={yearRepetitionDisplay}
          onChange={(e) => handleSelectChange(e.target.value, rules.display_options, setYearRepetitionDisplay, setYearRepetitionDisplayDescription)}
        >
          <option value="">Select a display option</option>
          {rules.display_options?.map((option) => (
            <option key={option.option_name} value={option.option_name}>
              {option.option_name}
            </option>
          ))}
        </select>
        {yearRepetitionDisplayDescription && (
          <p className="description-text">
            <i className="info-icon fas fa-info-circle"></i> {yearRepetitionDisplayDescription}
          </p>
        )}
      </div>

      {/* Course Repeat Policy */}
      <div className="field-group">
        <label>
          Course Repeat Policy
          <i className="info-icon fas fa-info-circle" title={getInfoTooltip("Course Repeat Policy")}></i>
        </label>
        <select
          value={courseRepeat}
          onChange={(e) => handleSelectChange(e.target.value, rules.course_repeat_rules, setCourseRepeat, setCourseRepeatDescription)}
        >
          <option value="">Select a policy</option>
          {rules.course_repeat_rules?.map((rule) => (
            <option key={rule.rule_name} value={rule.rule_name}>
              {rule.rule_name}
            </option>
          ))}
        </select>
        {courseRepeatDescription && (
          <p className="description-text">
            <i className="info-icon fas fa-info-circle"></i> {courseRepeatDescription}
          </p>
        )}
      </div>

      {/* Lab Course Repeat */}
      <div className="field-group">
        <label>
          Lab Course Repeat
          <i className="info-icon fas fa-info-circle" title={getInfoTooltip("Lab Course Repeat")}></i>
        </label>
        <select
          value={labCourseRepeat}
          onChange={(e) => handleSelectChange(e.target.value, rules.course_repeat_rules, setLabCourseRepeat, setLabCourseRepeatDescription)}
        >
          <option value="">Select a policy</option>
          {rules.course_repeat_rules?.map((rule) => (
            <option key={rule.rule_name} value={rule.rule_name}>
              {rule.rule_name}
            </option>
          ))}
        </select>
        {labCourseRepeatDescription && (
          <p className="description-text">
            <i className="info-icon fas fa-info-circle"></i> {labCourseRepeatDescription}
          </p>
        )}
      </div>

      {/* Course Repeat & Supplementary Display */}
      <div className="field-group">
        <label>
          Course Repeat & Supplementary Display
          <i className="info-icon fas fa-info-circle" title={getInfoTooltip("Course Repeat & Supplementary Display")}></i>
        </label>
        <select
          value={courseRepeatAndSupplementaryDisplay}
          onChange={(e) => handleSelectChange(e.target.value, rules.display_options, setCourseRepeatAndSupplementaryDisplay, setCourseRepeatAndSupplementaryDisplayDescription)}
        >
          <option value="">Select a display option</option>
          {rules.display_options?.map((option) => (
            <option key={option.option_name} value={option.option_name}>
              {option.option_name}
            </option>
          ))}
        </select>
        {courseRepeatAndSupplementaryDisplayDescription && (
          <p className="description-text">
            <i className="info-icon fas fa-info-circle"></i> {courseRepeatAndSupplementaryDisplayDescription}
          </p>
        )}
      </div>
          <label>SPI Formula:
                                <i className="info-icon fas fa-info-circle" title={getInfoTooltip("SPI Formula")}></i>
</label>
          <select value={spiFormula} onChange={(e) => setSpiFormula(e.target.value)}>
          <option value="">Select a formula</option>
          {rules.spi_formulas?.map((formula) => (
            <option key={formula.formula_name} value={formula.formula_name}>
              {formula.formula_name}
            </option>
          ))}          </select>

         {/* Round Off Limit for Decimal Places */}
             <label>
        Round to Decimal Places:
        <i className="info-icon fas fa-info-circle" title={getInfoTooltip("Round to Decimal Places")}></i>
      </label>
      <input
        type="number"
        value={decimalPlaces}
        onChange={(e) => setDecimalPlaces(Math.max(0, parseInt(e.target.value) || 0))} // Set minimum to 0
        min="0"
      />
          {/* SPI and CPI Names */}
          <label>SPI Name:
                                <i className="info-icon fas fa-info-circle" title={getInfoTooltip("SPI Name")}></i>
</label>
          <input
            type="text"
            value={spiName}
            onChange={(e) => setSpiName(e.target.value)}
          />
          <label>CPI Name:
                                <i className="info-icon fas fa-info-circle" title={getInfoTooltip("CPI Name")}></i>
</label>
          <input
            type="text"
            value={cpiName}
            onChange={(e) => setCpiName(e.target.value)}
          />

          {/* Batch Year Input */}
          <label>Batch Year:
                                <i className="info-icon fas fa-info-circle" title={getInfoTooltip("Batch Year")}></i>
</label>
          <input
            type="number"
            value={batchYear}
            onChange={(e) => setBatchYear(e.target.value)}
          />

          {/* Example Input and Output */}

        </div>
      )}

      {/* JSON Textarea for setting grading system */}
      {isUsingJson && (
        <div>
          <label>Set Grading System (JSON format):</label>
          <textarea
            className="json-text-area"
            rows="10"
            value={gradingSystemJson}
            onChange={(e) => setGradingSystemJson(e.target.value)}

          />
        </div>
      )}


          <div className="button-container">
      <button onClick={handleSubmit}>Set Grading System</button>
      </div>
    </div>
  );
};

export default GradingConfig;

