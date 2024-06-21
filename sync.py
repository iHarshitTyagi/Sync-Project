### Outline of the Data Processing Script

#### 1. **Loading Initial Data Sources**
   - **Master File (`SPPR_FCOK_Master.xlsx`)**:
     - Provides key identifiers and initial date ranges for SBPR (Service Bulletin Parts).
   - **FPCR Dump Data (`FPCR Dump Data.xlsx`)**:
     - Contains detailed FPCR records that will be merged with the master file to enrich data with additional attributes.

#### 2. **Merging and Formatting Data**
   - **Merging Master File with FPCR Data**:
     - Combines data from the master file with the FPCR dump to align date ranges and other attributes.
   - **Converting Date Formats**:
     - Ensures date columns ('Earliest' and 'Latest') are in a standardized datetime format for further operations.

#### 3. **Loading and Processing FTIR Data**
   - **FTIR Categorization Files**:
     - Latest FTIR categorization file from a specified directory provides categorization of SBPR items.
   - **Aggregating FTIR Dates**:
     - Groups FTIR data by SBPR number to compute minimum and maximum categorization dates.

#### 4. **Merging FTIR Data**
   - **Combining FPCR and FTIR Data**:
     - Merges the aggregated FTIR dates with the previously combined FPCR data.
   - **Determining Final Date Ranges**:
     - Calculates the minimum 'Earliest' and maximum 'Latest' dates from both datasets for each SBPR.

#### 5. **Saving Intermediate Results**
   - **Exporting Aggregated Dates**:
     - Saves the computed earliest and latest dates per SBPR to an Excel file for further reference.

#### 6. **Handling Sales Model Codes**
   - **Splitting and Exploding Sales Model Codes**:
     - Breaks down multi-model entries into individual model codes and cleans the data for each SBPR entry.

#### 7. **Loading and Processing Sales Data**
   - **Vehicle Dispatch Data**:
     - Provides monthly sales data for various models which will be used to calculate total sales over specified date ranges.
   - **Formatting Sales Data**:
     - Prepares sales data by setting appropriate headers and indices for easy integration with SBPR data.

#### 8. **Calculating Total Sales**
   - **Iterating Over SBPR Entries**:
     - For each SBPR record, calculates the total sales for the corresponding model within the defined date range.

#### 9. **Aggregating and Merging Sales Data**
   - **Grouping and Aggregating Sales**:
     - Aggregates total sales by SBPR and merges with the main dataset to include sales data.
   - **Combining with Original FPCR Data**:
     - Integrates the aggregated sales data with the original FPCR data for complete records.

#### 10. **Calculating Quality Metrics**
    - **PPM and OR Calculations**:
      - Computes Parts Per Million (PPM) and Occurrence Rate (OR) using FTIR counts and total sales data.

#### 11. **Loading Department Mapping Data**
    - **Department Mapping (`Department Mapping.xlsx`)**:
      - Maps segments to their respective departments to categorize SBPR entries.
    - **Updating Department Information**:
      - Applies department mapping to SBPR entries based on their segmentation.

#### 12. **Loading and Merging Part Information**
    - **FPCR Vendor Data**:
      - Latest file with additional part information such as part name, root cause, and countermeasures.
    - **Merging Part Information**:
      - Integrates part data with the SBPR dataset to enrich records with detailed part-related attributes.

#### 13. **Final Data Enhancements**
    - **Categorizing Countermeasures**:
      - Adds a categorical field indicating presence or absence of countermeasures.
    - **Binning PPM Values**:
      - Segments PPM values into predefined bins for easier analysis.
    - **Cleaning Department Data**:
      - Standardizes department names by removing prefixes.

#### 14. **Exporting Final Dataset**
    - **Saving to CSV**:
      - Exports the fully processed and enriched dataset to a CSV file for further analysis or reporting.

### Files Used
1. **`SPPR_FCOK_Master.xlsx`**: Provides initial SBPR identifiers and date ranges.
2. **`FPCR Dump Data.xlsx`**: Contains detailed FPCR records for merging with master data.
3. **`FTIR_Categorization` Directory**: Contains categorization files for FTIR data, selecting the most recent one.
4. **`Vehicle Dispatch Data.xlsx`**: Sales data file used to calculate total sales for SBPR models.
5. **`Department Mapping.xlsx`**: Maps SBPR segments to corresponding departments.
6. **`FPCR_Vendor_Wise` Directory**: Provides part-related information from the most recent file in the directory.

### Overall Process
- The script sequentially loads, processes, and merges data from various sources.
- It calculates key metrics such as total sales, PPM, and OR for SBPR entries.
- The final dataset is enriched with department and part information, standardized, and categorized.
- The processed dataset is then saved for use in reporting or further analysis.