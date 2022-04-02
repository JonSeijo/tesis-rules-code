select * from protein where filename like "%p25963%"

select * from rule_coverage where idProtein = 2

select count(*) from rule

select * from protein

-- reglas que cubren a una proteína
select 
	-- p.filename,
	r.rule, 
	--CASE WHEN rc.coverageMode = 3 THEN 'Antecedente & Consecuente'
    --        WHEN rc.coverageMode = 2 THEN 'Consecuente'
    --        WHEN rc.coverageMode THEN 'Antecedente'
	--END as coverageMode,
	-- rc.idProtein,
	-- rc.idRule,
	CASE WHEN r.ruleType = 1 THEN 'Overlapping'
            WHEN r.ruleType = 2 THEN 'AddsInfo'
            WHEN r.ruleType THEN 'N/A'
	END as ruleType,
	rc.fraction from rule r
	inner join rule_coverage rc on rc.idRule = r.idRule and rc.idProtein = 11598
	inner join protein p on rc.idProtein = p.idProtein
	
-- reglas que aparezcan en antecedente o exclusivamente en consecuente (pero no en ambas) -- TODO!
select r.idRule, r.rule from rule r
	inner join rule_coverage rc on rc.idRule = r.idRule and rc.coverageMode != 3
	order by r.idRule ASC


--proteinas que no son cubiertas por ninguna regla	

select * 
from protein p
where NOT EXISTS (select * from rule_coverage rc where rc.idProtein = p.idProtein)

-- 11598 -> ikba
	
	
-- MFQAAERPQEWAMEGPRDGLKKERLLDDRHDSGLDSMKDEEYEQMVKELQEIRLEPQEVPRGSEPWKQQLTEDGDSFLHLAIIHEEKALTMEVIRQVKGDLAFLNFQNNLQQTPLHLAVITNQPEIAEALLGAGCDPELRDFRGNTPLHLACEQGCLASVGVLTQSCTTPHLHSILKATNYNGHTCLHLASIHGYLGIVELLVSLGADVNAQEPCNGRTALHLAVDLQNPDLVSLLLKCGADVNRVTYQGYSPYQLTWGRPSTRIQQQLGQLTLENLQMLPESEDEESYDTESEFTEFTEDELPYDDCVFGGQRLTL