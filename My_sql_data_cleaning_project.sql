-- DATA CLEANING
  SELECT *
  FROM layoffs;  
  -- 1. REMOVE DUPLICATES
  -- 2. STANDARIZE THE DATA
  -- 3. NULL VALUES OR BLANK VALUES
  -- 4. REMOVE ANY COLUMNS OR ROWS
  CREATE TABLE layoffs_staging
  LIKE layoffs;
  SELECT *
  FROM layoffs_staging;
  INSERT layoffs_staging
  SELECT *
  FROM layoffs;
  
  -- IDENTIFY DUPLICATES
  SELECT *, ROW_NUMBER() OVER(PARTITION BY company, industry, total_laid_off , 
   percentage_laid_off, `date`) AS row_num
  FROM layoffs_staging;
  WITH duplicate_cte AS
  (  SELECT *, ROW_NUMBER() OVER(PARTITION BY company, location, industry, total_laid_off , 
   percentage_laid_off, `date`, stage, country, funds_raised_millions) AS row_num
  FROM layoffs_staging) 
  SELECT *
  FROM duplicate_cte 
  WHERE row_num > 1;
 SELECT * 
  FROM layoffs_staging
  WHERE location = 'Ibadan';
  -- DELETING DUPLICATES
WITH duplicate_cte AS
  (  SELECT *, ROW_NUMBER() OVER(PARTITION BY company, location, industry, total_laid_off , 
   percentage_laid_off, `date`, stage, country, funds_raised_millions) AS row_num
  FROM layoffs_staging) 
  DELETE 
  FROM duplicate_cte 
  WHERE row_num > 1;
  
  CREATE TABLE `layoffs_staging2` (
  `company` text,
  `location` text,
  `industry` text,
  `total_laid_off` int DEFAULT NULL,
  `percentage_laid_off` text,
  `date` text,
  `stage` text,
  `country` text,
  `funds_raised_millions` int DEFAULT NULL,
  `row_num`int
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
SELECT *
 FROM layoffs_staging2 
 WHERE row_num > 1; 
 INSERT INTO layoffs_staging2
 SELECT *, ROW_NUMBER() OVER(PARTITION BY company, location, industry, total_laid_off , 
   percentage_laid_off, `date`, stage, country, funds_raised_millions) AS row_num
  FROM layoffs_staging;
  DELETE
 FROM layoffs_staging2 
 WHERE row_num > 1; 
 SELECT *
 FROM layoffs_staging2 
 WHERE row_num > 1; 
 -- STANDARDIZING DATA
  SELECT  company, TRIM(company)
  FROM layoffs_staging2;
  UPDATE layoffs_staging2
  SET company = TRIM(company);
  SELECT DISTINCT country, TRIM(TRAILING '.' FROM country)
  FROM layoffs_staging2 
  order by 1;
  UPDATE layoffs_staging2
  SET country = TRIM(TRAILING '.' FROM country)
  WHERE country LIKE 'United States%'; 
  SELECT `date`
  
 -- ,str_to_date(`date`, '%m/%d/%Y')
  FROM layoffs_staging2;
  UPDATE layoffs_staging2
  SET `date` = str_to_date(`date`, '%m/%d/%Y');
  ALTER TABLE layoffs_staging2
  MODIFY `date` DATE ;
  -- NULL AND BLANK VALUES
  SELECT *
  FROM layoffs_staging2
  WHERE total_laid_off IS NULL
  AND percentage_laid_off IS NULL;
    SELECT *
  FROM layoffs_staging2
  WHERE industry IS NULL
  OR industry = '';
-- DELETING COLUMNS/ROWS
SELECT *
  FROM layoffs_staging2
  WHERE total_laid_off IS NULL
  AND percentage_laid_off IS NULL;
  DELETE
  FROM layoffs_staging2
  WHERE total_laid_off IS NULL
  AND percentage_laid_off IS NULL; 
  ALTER TABLE layoffs_staging2
  DROP COLUMN row_num;
  SELECT *
  FROM layoffs_staging2;
  -- EXPLORATORY DATA ANALYSIS 
  SELECT *
  FROM layoffs_staging2
 -- ORDER BY 6
  ;
  SELECT MAX(total_laid_off), MAX(percentage_laid_off), MAX(funds_raised_millions)
  FROM layoffs_staging2;
   SELECT *
  FROM layoffs_staging2
  WHERE percentage_laid_off = 1 
  -- ORDER BY total_laid_off DESC
  ORDER BY funds_raised_millions DESC;
 SELECT company, SUM(total_laid_off)
  FROM layoffs_staging2
  GROUP BY company 
   -- ORDER BY 2 (2 STAND FOR SECOND COLUMN)DESC
  -- ORDER BY SUM(total_laid_off) DESC;
  ORDER BY 2 DESC;
  SELECT MIN(`date`), MAX(`date`)
  FROM layoffs_staging2;
   SELECT industry , SUM(total_laid_off)
  FROM layoffs_staging2
  GROUP BY industry
  ORDER BY 2 DESC;
   SELECT country, SUM(total_laid_off)
  FROM layoffs_staging2
  GROUP BY country
  ORDER BY 2 DESC;
    SELECT YEAR(`date`), SUM(total_laid_off)
  FROM layoffs_staging2
  GROUP BY YEAR(`date`)
  ORDER BY 2 DESC;
   SELECT stage, SUM(total_laid_off)
  FROM layoffs_staging2
  GROUP BY stage
  ORDER BY 2 DESC;
   SELECT SUBSTRING(`date`,1,7) AS `MONTH` ,SUM(total_laid_off)
 FROM layoffs_staging2
 WHERE SUBSTRING(`date`,1,7)  IS NOT NULL
  GROUP BY `MONTH`
 ORDER BY 1 ASC ;
WITH Rolling_total AS
(
 SELECT SUBSTRING(`date`,1,7) AS `MONTH`,SUM(total_laid_off) AS total_off
 FROM layoffs_staging2
 WHERE SUBSTRING(`date`,1,7)  IS NOT NULL
  GROUP BY `MONTH`
 ORDER BY 1 ASC 
)
SELECT `MONTH`, total_off,SUM(total_off) OVER(ORDER BY `MONTH`) AS rolling_total
FROM Rolling_total;
 SELECT company, YEAR(`date`), SUM(total_laid_off)
  FROM layoffs_staging2
  GROUP BY company, YEAR(`date`)
    ORDER BY company ASC
    -- ORDER BY 3 DESC 
    ;
    WITH Company_Year(company, years, total_laid_off)  AS
    (
     SELECT company, YEAR(`date`), SUM(total_laid_off)
  FROM layoffs_staging2
  GROUP BY company, YEAR(`date`)
    ), Company_Year_Rank AS
    (SELECT *, DENSE_RANK() OVER(PARTITION BY years ORDER BY total_laid_off DESC)
    AS Ranking
    FROM Company_Year
     )
     SELECT *
     FROM Company_Year_Rank
     WHERE Ranking <= 5;
     -- CONTINUATION
     SELECT *
     FROM layoffs_staging2;
     WITH industry_Year(country, years, total_laid_off)  AS
    (
     SELECT industry, YEAR(`date`), SUM(total_laid_off)
  FROM layoffs_staging2
  GROUP BY industry, YEAR(`date`)
    )
    -- SELECT *
     -- FROM Industry_Year;
     ,
   industry_Year_Rank AS
    (SELECT *, DENSE_RANK() OVER(PARTITION BY years ORDER BY total_laid_off DESC)
    AS Ranking
    FROM industry_Year
     )
     SELECT *
     FROM industry_Year_Rank
     WHERE Ranking <= 5;
      WITH country_Year(company, years, total_laid_off)  AS
    (
     SELECT country, YEAR(`date`), SUM(total_laid_off)
  FROM layoffs_staging2
  GROUP BY country, YEAR(`date`)
    ), country_Year_Rank AS
    (SELECT *, DENSE_RANK() OVER(PARTITION BY years ORDER BY total_laid_off DESC)
    AS Ranking
    FROM country_Year
     )
     SELECT *
     FROM 
     country_Year_Rank
     WHERE Ranking <= 10;
     -- NUMBERS
     SELECT *
     FROM layoffs_staging2
     WHERE total_laid_off IS NOT NULL OR '.' ;
      SELECT *
     FROM layoffs_staging2
     WHERE percentage_laid_off IS NOT NULL OR '.';
SELECT *
     FROM layoffs_staging2
     WHERE total_laid_off IS NOT NULL AND percentage_laid_off IS NOT NULL;
     CREATE TABLE `layoffs_staging3` (
  `company` text,
  `location` text,
  `industry` text,
  `total_laid_off` int DEFAULT NULL,
  `percentage_laid_off` text,
  `date` date DEFAULT NULL,
  `stage` text,
  `country` text,
  `funds_raised_millions` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
 INSERT INTO layoffs_staging3
SELECT *
     FROM layoffs_staging2
     WHERE total_laid_off IS NOT NULL AND percentage_laid_off IS NOT NULL;
     SELECT *
     FROM layoffs_staging3;
--     FROM layoffs_staging2
-- WHERE total_laid_off IS NOT NULL AND percentage_laid_off IS NOT NULL 
--     AND funds_raised_millions IS NOT NULL;
     
     
  
  
  
  
  

  