package pyomoforge;

/*
 * #%L
 * PyomoForge
 * 
 * Module name: com.orange.common:pyomoforge
 * Version:     1.0
 * Created:     2022-08-24
 * %%
 * Copyright (C) 2022 Orange
 * %%
 * The license and distribution terms in 'LGPL-3.0+' for this file may be found 
 * in the file 'gnu lesser general public license v3.0 or later - license.txt' in this distribution 
 * or LICENSE.txt or at http://www.gnu.org/licenses/lgpl-3.0-standalone.html.
 * #L%
 */

import java.util.Arrays;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.JScrollPane;

import org.antlr.v4.runtime.ANTLRInputStream;
import org.antlr.v4.runtime.CharStream;
import org.antlr.v4.runtime.CommonTokenStream;
import org.antlr.v4.runtime.TokenStream;
import org.antlr.v4.runtime.tree.ParseTree;
import org.antlr.v4.gui.TreeViewer;


/**
 * LaTeX world!
 *
 */
public class App 
{
    public static void main( String[] args )
    {
        // String in = "m^{t}_{s,g} \\leq \\overline{M}_{g} * z^{t}_{s,g} \\forall t \\in T, \\forall s \\in S, \\forall g \\in G, (4.38)";
        // String in = "m^{t-1}_{s,g} \\leq m^{t}_{s,g} \\forall t \\in T, \\forall s \\in S, \\forall g \\in G, (4.39)";
        // String in = "m^{\\overline{t}}_{s,g} \\leq M0_{s,g} + \\overline{M}_{g} \\times InvM_{g} \\forall s \\in S, \\forall g \\in G, (4.40)";
        // String in = "\\sum_{a \\in A} \\sum_{s \\in S} u^{t}_{a,o,s,g} \\leq CP_{o,g} \\times \\sum_{a \\in A} \\overline{U}^t_{a,o} \\forall t \\in T, \\forall g \\in G, \\forall o \\in O, (4.43)";
        // String in = "u^t_{a,NO} = u^{t-1}_{a,NO} + N^t_oNO \\times UTOT^{t-1}_a - \\sum_{o \\in OminusNO} \\sum_{σ \\in K} \\sum_{c \\in C} f_{σ,c} * π^t_{σ,c,a,o} \\forall t \\in Tminus0, \\forall a \\in A, (4.48)";
        // String in = "\\sum_{s \\in S} \\sum_{a \\in A}  u^{\\overline{t}}_{a,NO,s,NG} \\geq \\underline{QoE} \\times \\sum_{a \\in A} UTOT^{\\overline{t}}_a, (4.49)";
        // String in = "min (\\sum_{t \\in T} \\sum_{σ \\in K} \\sum_{c \\in C} \\sum_{a \\in A} \\sum_{o \\in OminusNO} σ * f_{σ,c,o} * π^{t}_{σ,c,a,o}) + (\\sum_{s \\in S} \\sum_{g \\in G} CM_{g} * (m^{\\overline{t}}_{s,g} - M^{0}_{s,g})) + (\\sum_{s \\in S} \\sum_{g \\in G} CA_{g} * (z^{\\overline{t}}_{s,g} - Z^{0}_{s,g}))";
	    // String in = "\\begin{align*}\nmin \\sum_{j \\in J} y_{j} & \\\\\ns.t. & \\\\\n & \\sum_{i \\in I} c_{i} * x_{i,j} \\leq C * y_{j} & \\forall j \\in J, & (1) \\\\\n & \\sum_{j \\in J} x_{i,j} = 1 & \\forall i \\in I, & (2) \\\n\\end{align}";
	    // String in = "min \\sum_{j \\in J} y_{j}\ns.t.\n\\sum_{i \\in I} c_{i} * x_{i,j} \\leq C * y_{j} \\forall j \\in J, (1)\n\\sum_{j \\in J} x_{i,j} = 1 \\forall i \\in I, (2)";
	    // String in = "\\max 0 % this is a comment!\nst.";
        //String in = "\\begin{align}\n\\min &\\\\\nst. &\\\\\n&  m^t_{s,g} =\\sum\\limits_{b \\in B} m^t_{s,g,b}, \\forall t \\in \\TZ,  \\forall \\sis, \\forall \\gig  \\label{summ_4_31} \\";
        // String in = "m^t_{s,g} =\\sum\\limits_{b \\in B} m^t_{s,g,b}, \\forall t \\in TZ,  \\forall s \\in S, \\forall g \\in G  \\label{summ_4_31}  ";
        // String in = "\\newcommand{\\GP}{\\mathcal{G}}\n"  + 
        // "\\newcommand{\\gig}{g \\in \\GP}\n"  + 
        // "\\newcommand{\\TZ}{\\mathcal{T} \\cup \\{0\\}}\n"  + 
        // "\\newcommand{\\sis}{s \\in \\SI}\n"  + 
        // "\\begin{align}\n"  + 
        // " \\min 0 & \\\\\n"  + 
        // " st. & \\\\\n"  + 
        // "&  incr^t_{s,g,b} \\geq m^t_{s,g,b} - m^{t-1}_{s,g,b},  \\forall t \\in \\TZ,  \\forall \\sis, \\forall \\gig, \\forall  b\\in \\mathcal{B} \\label{eqincr_4_32}\\\\\n"  + 
        // "\\end{align} \n";
        // String in = "α^\\overline{t} \\geq  \\underline{α}, (4.50)";
        // String in = "vars &\\nonumber \\\\\n        &  u^t_{a,o,s,g} \\geq 0 ,   \\forall  t\\in \\T,\\forall (a,o,s,g) \\in \\mathcal{AOSG},  \\label{def_u_filtered} \\\\\n  &\\alpha^{t} \\geq 0 ,\\forall t \\in T  \\cup\\{0\\}\\\\";
        // String in = "y_{p}^{t} \\in \\{0,1\\}";
        // String in = "min \\sum_{j \\in J} y_{j}\ns.t.\n\\sum_{i \\in I} c_{i} * x_{i,j} \\leq C * y_{j} \\forall j \\in J, (1)\n\\sum_{j \\in J} x_{i,j} = 1 \\forall i \\in I, (2)\nvars\ny_{j} \\in \\mathbb{N}, \\forall j \\in J\nx_{i,j} \\in \\mathbb{N}, \\forall i \\in I, \\forall j \\in J";
        String in = "vars &\\nonumber \\\\\nx_{i,j} \\in \\mathbb{N}, \\forall j \\in J, \\forall i \\in I \ny_{j} \\in \\mathbb{N}, \\forall j \\in J ";

	    System.out.println(in);
        CharStream stream = new ANTLRInputStream(in);
        LaTeXLexer lexer  = new LaTeXLexer(stream);   
        TokenStream tokenStream = new CommonTokenStream(lexer);
        LaTeXParser parser = new LaTeXParser(tokenStream);
        ParseTree tree = parser.vardefs(); 
        // ParseTree tree = parser.objective(); 
	    // ParseTree tree = parser.model(); 


        //show AST in console
        System.out.println(tree.toStringTree(parser));

        //show AST in GUI
        JFrame frame = new JFrame("Antlr AST");
        JPanel panel = new JPanel();
        JScrollPane scrollPane = new JScrollPane(panel, 
            JScrollPane.VERTICAL_SCROLLBAR_ALWAYS, 
            JScrollPane.HORIZONTAL_SCROLLBAR_ALWAYS);
        TreeViewer viewer = new TreeViewer(Arrays.asList(
                parser.getRuleNames()),tree);
        viewer.setScale(1.5); // Scale a little
        panel.add(viewer);
        frame.add(scrollPane);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.pack();
        frame.setVisible(true);
    }
}
